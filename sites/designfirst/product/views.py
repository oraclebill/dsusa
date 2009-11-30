from datetime import datetime
from decimal import Decimal
from hashlib import sha1
import json
import logging

from paypal.pro.views import PayPalPro            
from paypal.pro.signals import payment_was_successful, payment_was_flagged
from paypal.pro.forms import PaymentForm

from django.core import serializers
from django.db import transaction
from django.db.models import Sum        
from django.http import HttpResponseRedirect, HttpResponseServerError, HttpResponse
# from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from utils import make_site_url
from accounting.models import register_purchase
from models import Product
from customer.models import Invoice
from customer.auth import active_dealer_only
    
import cart as shcart
    
logger = logging.getLogger('product.views')

@transaction.commit_on_success
def paypal_success_callback(sender, **kwargs):
    logger.debug('paypal_success_callback: sender=%s, kwargs=%s' % (sender, kwargs))
    invnum = sender['invnum']    
    invoice = Invoice.objects.get(pk=invnum)
    invoice.status = Invoice.Const.PAID
    invoice.save()
    register_purchase(invoice.id, invoice.customer, invoice.total, invoice.total_credit)
payment_was_successful.connect(paypal_success_callback)
        
@transaction.commit_on_success
def paypal_failure_callback(sender, **kwargs):
    logger.debug('paypal_failure_callback: sender=%s, kwargs=%s' % (sender, kwargs))
    invnum = sender['invnum']    
    invoice = Invoice.objects.get(pk=invnum)
    invoice.status = Invoice.Const.CANCELLED
    invoice.save()
payment_was_flagged.connect(paypal_failure_callback)


def product_detail(request, prodid):
    user = request.user
    if user is None or not user.is_authenticated():
        return HttpResponseRedirect('/') ## FIXME
    
    account         = request.user.get_profile().account
    product         = Product.objects.get(pk=prodid)
    price_retail    = product.base_price
        
    return render_to_response( "product/product_detail.html", 
        locals(), context_instance=RequestContext(request) )

@login_required
@active_dealer_only
def add_cart_product(request, prodid):
    pass

@login_required
@active_dealer_only
def remove_cart_product(request, prodid):
    pass
    
@login_required
@active_dealer_only
def select_products(request, template="product/product_selection.html", extra_context={}):
    "Provides the template with a product list and the cart item list, combined for users purchase."
    user = request.user
    if user is None or not user.is_authenticated():
        return HttpResponseRedirect('/') ## FIXME with decorators..
    
    account = request.user.get_profile().account

    # post means they've selected somethign to purchase. put the items in your 'cart' and go to confirm stage
    cart = shcart.get_cart_from_request(request)

    if request.method == 'POST':
        shcart.destroy_cart(cart)        
        cart_empty = True        
        product_quantities = [ (int(id[6:]), int(count or 0)) 
                                for (id, count) 
                                    in request.POST.items() 
                                        if id.startswith('count_') and int(count or 0)]
        logger.debug('product_quantities\n\n\n\n %s, %s, %s', product_quantities, bool(product_quantities), len(product_quantities))
        if product_quantities:      
            cart_empty = False                  
            for prod_id, qty in product_quantities:
                shcart.add_item(cart, prod_id, int(qty))                
                
        if '_purchase' in request.POST:            
            if cart_empty:
                errors = ["You cannot checkout until you purchase at least one item!"]
            else:
                # go to confirmation page
                return HttpResponseRedirect(reverse("confirm_purchase_selections"))
        return HttpResponseRedirect(reverse('select_products'))

    cart_items = shcart.get_cart_items(cart)
    cart_total = sum([i.extended_price for i in cart_items])
    item_hash = dict()
    for item in cart_items:
        item_hash[item.product_id] = item

    products = Product.objects.all()
    pricelist = [ (product, item_hash.get(product.id, 0)) for product in products]
        
    # the following won't work, since extended_price is not a database field...
    # cart_total = cart_items.aggregate(Sum('extended_price')).get('extended_price__sum', 0)
        
    logger.debug('cart items: %s', cart_items)
    context = {'pricelist': pricelist, 'cart_items': cart_items, 'cart_total': cart_total}
    context.update(extra_context)
    return render_to_response( template, context, context_instance=RequestContext(request) )
                
                
def render_cart(request, template_name='product/cart_fragment.html'):
    cart = shcart.get_cart_from_request(request)
    cart_items = shcart.get_cart_items(cart)
    if request.is_ajax():
        response = serializers.serialize("json", cart_items)
        return HttpResponse(response, content_type='application/json')
    return render_to_response(template_name, {'cart_items': cart_items} )        
        
def render_product_list(request, template_name='product/product_list_fragment.html'):
    all_prods = Product.objects.all()
    base_prods = all_prods.filter(product_type=Product.Const.BASE)
    package_prods = all_prods.filter(product_type=Product.Const.PACKAGE)
    option_prods = all_prods.filter(product_type=Product.Const.OPTION)
    pkgoption_prods = all_prods.filter(product_type=Product.Const.PACKAGE + Product.Const.OPTION)
    subscription_prods = all_prods.filter(product_type=Product.Const.SUBSCRIPTION)
    if request.is_ajax():
        response = serializers.serialize("json", locals())
        return HttpResponse(response, content_type='application/json')
    return render_to_response(template_name, locals() )                                    
        
@login_required
@active_dealer_only
def confirm_selections(request):
    "Display the selected products and pricing info and identify payment mechanism."
    account = request.user.get_profile().account

    cart = shcart.get_cart_from_request(request)
    cart_items = shcart.get_cart_items(cart)
    cart_total = sum([i.extended_price for i in cart_items])
              
    return render_to_response( "product/product_selection_review.html", locals(), 
        context_instance=RequestContext(request) )


@login_required
@active_dealer_only
def paypal_checkout(request,  
                    collection_template='product/paypal_checkout.html', 
                    confirmation_template='product/paypal_checkout.html', 
                    success_url=None,
                    form_class=PaymentForm, 
                    extra_context=None):    
    """
    Checkout the current shopping cart via paypal..
    
    Template context:
        - phase
        - account
        - form        
        - cart_items
    
    Checkout consists of three steps:
        1) collect credit card info (while reviewing order info)
           - on submit we do local validation. cycle until this process succeeds or user quits.
           - user can select paypal checkout from the point which initiates alternate flow (managed by the paypal plugin)
        2) display card info and order info for final review
           - on submit we 
               - create an invoice from the currnent cart
               - destroy the current cart
               - send card / order info to payment gateway for processing
           - if processing succeeds
               - find the invoice and mark it paid
           - else if it fails
               - find the invoice and mark it 'failed'. attach failure info to invoice for tracking        
        3) display invoice and success/failure message         
    
    If the user elects paypal checkout, there is an alternate flow.
    """
    
    def item_from_invoice(inv):
        item = {
            "amt":          inv.total,
            "invnum":       inv.id,
            "custom":       request.session.session_key,    # for debugging
            "desc":         inv.description,
            "cancelurl":    make_site_url(reverse('select_products')),     # Express checkout cancel url
            "returnurl":    make_site_url(reverse('home'))     # Express checkout return url
        } 
        return item

    phase = request.GET.get('p', 'collect')
    logger.debug('entered paypal_checkout: phase=%s, GET=%s, POST=%s', phase, request.GET, request.POST) 
    # gather some info we always need
    account = request.user.get_profile().account
    cart = shcart.get_cart_from_request(request)
    cart_items = shcart.get_cart_items(cart)
    template = collection_template
    
    if request.method == 'GET':
        # dieplay cc form
        form = form_class()
    elif request.method == 'POST':
        # validate the cc form. 
        form = form_class(request.POST, request.FILES) 
        if phase == 'collect':
            logger.debug(' paypal_checkout: collect phase...') 
            if form.is_valid():
                template = confirmation_template
                phase = 'confirm'
        elif phase == 'confirm':
            logger.debug(' paypal_checkout: confirm phase...') 
            if form.is_valid():
                logger.debug(' paypal_checkout: confirm phase valid...') 
                invoice = shcart.create_invoice_from_cart(cart, account, request.user)
                response = form._process(request, item_from_invoice(invoice))
                logger.debug(' paypal_checkout: payment response: %s', response) 
                if not response.flag:      
                    invoice.status = Invoice.Const.PAID
                    invoice.save()
                    register_purchase(invoice.id, invoice.customer, invoice.total, invoice.total_credit)          
                    request.user.message_set.create(message='Payment processed successfully - thanks!')
                    if success_url:
                        return HttpResponseRedirect(success_url)
                else:
                    invoice.status = Invoice.Const.CANCELLED
                    #invoice.notes = '%s: %s' % (response.flag_code, response.flag_info)
                    notes = '%s: %s' % (response.flag_code, response.flag_info)
                    invoice.save()
                    request.user.message_set.create(message='Payment processing error - %s' % notes)
                return HttpResponseRedirect(reverse('invoice-detail', kwargs={'object_id': invoice.id}))
            else:
                phase = 'collect'  # back up...
        else:
            return HttpResponseServerError("Internal error - illegal program state: %s" % phase)            
                
    context = locals()
    context.pop('request')
    logger.debug(' paypal_checkout: exiting with context: %s', context) 
    return render_to_response( template, context, context_instance=RequestContext(request))            
        
        
@login_required
@active_dealer_only
@transaction.commit_on_success
def checkout(request, success_url=''):
    """
    Display and/or collect payment information while displaying a summary of products to be purchased.
    
    Checkout consists of three steps:
        1) collect credit card info (while reviewing order info)
           - on submit we do local validation. cycle until this process succeeds or user quits.
           - user can select paypal checkout from the point which initiates alternate flow (managed by the paypal plugin)
        2) display card info and order info for final review
           - on submit we 
               - create an invoice from the currnent cart
               - destroy the current cart
               - send card / order info to payment gateway for processing
           - if processing succeeds
               - find the invoice and mark it paid
           - else if it fails
               - find the invoice and mark it 'failed'. attach failure info to invoice for tracking        
        3) display invoice and success/failure message         
    
    If the user elects paypal checkout, there is an alternate flow.
    """
    from models import CartItem
    #
    account = request.user.get_profile().account
    #
    # we're basically a wrapper around this view func... so lets configure it.
    view_func = PayPalPro(payment_template="product/checkout.html",
                    confirm_template="paypal/express_confirmation.html",
                    success_url=reverse('home')
    )   
    try:
        # if there's no NEW invoice, create one from current cart
        try:
            invoice = account.invoice_set.get(status=Invoice.Const.NEW)
            logger.debug('checkout: [%s] found pre-existing new invoice [%s]' % (request.session.session_key, invoice.id))
        except Invoice.DoesNotExist:
            sig = sha1(repr(datetime.now())).hexdigest()
            invoice = Invoice(id=sig, customer=account, status=Invoice.Const.NEW)
            invoice.description = "Web Purchase by '%s' on '%s'" % (request.user.email, datetime.now())
            cart_items = CartItem.objects.filter(session_key__exact=request.session.session_key)
            for item in cart_items:
                invoice.add_line(item.product.name, item.product.base_price, item.quantity)
                item.delete()
            # note - we are in transaction context.. save probably has no effect...
            invoice.save()
            logger.debug('checkout: [%s] created new invoice [%s]' % (request.session.session_key, invoice.id))
        #
        # if this is a post, we try to process the invoice.
        if request.method == "POST" or (request.method == "GET" and 'express' in request.GET):
            # change invoice status to pending
            invoice.status = Invoice.Const.PENDING
            # configure the paypal processor with invoice info.
            view_func.item = {
                "amt":          invoice.total,
                "invnum":       invoice.id,
                "custom":       request.session.session_key,    # for debugging
                "desc":         invoice.description,
                "cancelurl":    make_site_url(reverse('select_products')),     # Express checkout cancel url
                "returnurl":    make_site_url(reverse('home'))     # Express checkout return url
            }
            request.user.message_set.create(message='Thanks for your order!')
    except Exception as ex:
        transaction.rollback()
        errors = "Failed to create new invoice! (%s)" % ex
    else:
        transaction.commit()
    #
    view_func.context = locals()
#    logger.debug('checkout: session #%s: payment request for invoice [%s] submitted to paypal with item=%s, context=%s' % (
#        request.session.session_key,
#        invoice,
#        view_func.item,
#        view_func.context)
#    )
    return view_func(request)

