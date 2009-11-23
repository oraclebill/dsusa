from datetime import datetime
from decimal import Decimal
from hashlib import sha1
from pickle import dumps
import logging

from paypal.pro.views import PayPalPro            
from paypal.pro.signals import payment_was_successful, payment_was_flagged


from django.db import transaction
from django.db.models import Sum        
from django.http import HttpResponseRedirect
# from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.contrib.auth.models import User

from accounting.models import register_purchase
from models import Product,CartItem
from customer.models import Invoice 
    
logger = logging.getLogger('product.views')

@transaction.commit_on_success
def paypal_success_callback(sender, **kwargs):
    logger.debug('paypal_success_callback: sender=%s, kwargs=%s' % (sender, kwargs))
    invnum = sender['invnum']    
    invoice = Invoice.objects.get(pk=invnum)
    invoice.status = Invoice.PAID
    invoice.save()
    register_purchase(invoice.id, invoice.customer, invoice.total, invoice.total_credit)
payment_was_successful.connect(paypal_success_callback)
        
@transaction.commit_on_success
def paypal_failure_callback(sender, **kwargs):
    logger.debug('paypal_failure_callback: sender=%s, kwargs=%s' % (sender, kwargs))
    invnum = sender['invnum']    
    invoice = Invoice.objects.get(pk=invnum)
    invoice.status = Invoice.CANCELLED
    invoice.save()
payment_was_flagged.connect(paypal_failure_callback)


def make_site_url(request, path):
    from django.contrib.sites.models import Site
    scheme = request.is_secure() and 'https' or 'http'
    domain = Site.objects.get_current().domain.rstrip('/')    
    return '%s://%s/%s' % (scheme, domain, path.lstrip('/'))
    
def product_detail(request, prodid):
    user = request.user
    if user is None or not user.is_authenticated():
        return HttpResponseRedirect('/') ## FIXME
    
    account         = request.user.get_profile().account
    product         = Product.objects.get(pk=prodid)
    price_retail    = product.base_price
        
    return render_to_response( "product/product_detail.html", 
        locals(), context_instance=RequestContext(request) )
    
def select_products(request, template):
    "Display the product list and collect product id's for users purchase."
    user = request.user
    if user is None or not user.is_authenticated():
        return HttpResponseRedirect('/') ## FIXME with decorators..
    
    account = request.user.get_profile().account

    # post means they've selected somethign to purchase. put the items in your 'cart' and go to confirm stage
    if request.method == 'POST':
        cart_empty = True
        CartItem.objects.all().delete()
        product_quantities = [ (int(id[6:]), int(count or 0)) for (id, count) in request.POST.items() if id.startswith('count_') and int(count or 0)]
        if product_quantities:      
            cart_empty = False                  
            for prod_id, qty in product_quantities:
                item = CartItem(
                    session_key = request.session.session_key,
                    product = Product.objects.get(pk=prod_id),
                    quantity = int(qty)
                )
                item.save()
                
        if '_purchase' in request.POST:            
            if cart_empty:
                errors = ["You cannot checkout until you purchase at least one item!"]
            else:
                # go to confirmation page
                return HttpResponseRedirect(reverse("confirm_purchase_selections"))

    # using a aggregate here seems silly, but baffled as to how else to do this cleanly..
    pricelist = [ ( product, 
                    product.base_price, 
                    product.cartitem_set.aggregate(Sum('quantity')).get('quantity__sum') or 0
                  ) for product in Product.objects.all() ]
    
    cart_items = CartItem.objects.filter(session_key__exact=request.session.session_key)
    cart_total = sum([i.extended_price for i in cart_items])
    # the following won't work, since extended_price is not a database field...
    # cart_total = cart_items.aggregate(Sum('extended_price')).get('extended_price__sum', 0)
        
    return render_to_response( template, locals(), context_instance=RequestContext(request) )
                
def confirm_selections(request):
    "Display the selected products and pricing info and identify payment mechanism."
    account = request.user.get_profile().account

    cart_items = CartItem.objects.filter(session_key__exact=request.session.session_key)
    cart_total = sum([i.extended_price for i in cart_items])
              
    return render_to_response( "product/product_selection_review.html", locals(), 
        context_instance=RequestContext(request) )
    
@transaction.commit_on_success
def review_and_process_payment_info(request):
    "Display and/or collect payment information while displaying a summary of products to be purchased."    
    #
    account = request.user.get_profile().account
    #
    # we're basically a wrapper around this view func... so lets configure it.
    view_func = PayPalPro(payment_template="product/payment_info_review.html",     
                    confirm_template="paypal/express_confirmation.html",
                    success_url=reverse('home')
    )    
    try:        
        # if there's no NEW invoice, create one from current cart
        try:
            invoice = account.invoice_set.get(status=Invoice.NEW)
            logger.debug('review_and_process_payment_info: [%s] found pre-existing new invoice [%s]' % (request.session.session_key, invoice.id))
        except Invoice.DoesNotExist:
            sig = sha1(repr(datetime.now())).hexdigest()
            invoice = Invoice(id=sig, customer=account, status=Invoice.NEW)
            invoice.description = "Web Purchase by '%s' on '%s'" % (request.user.email, datetime.now())
            cart_items = CartItem.objects.filter(session_key__exact=request.session.session_key)    
            for item in cart_items:
                invoice.add_line(item.product.name, item.product.base_price, item.quantity)
                item.delete()
            # note - we are in transaction context.. save probably has no effect...
            invoice.save()    
            logger.debug('review_and_process_payment_info: [%s] created new invoice [%s]' % (request.session.session_key, invoice.id))
        #
        # if this is a post, we try to process the invoice.
        if request.method == "POST" or (request.method == "GET" and 'express' in request.GET):        
            # change invoice status to pending 
            invoice.status = Invoice.PENDING
            # configure the paypal processor with invoice info.
            view_func.item = {
                "amt":          invoice.total,
                "invnum":       invoice.id,
                "custom":       request.session.session_key,    # for debugging
                "desc":         invoice.description,
                "cancelurl":    make_site_url(request, reverse('select_products')),     # Express checkout cancel url
                "returnurl":    make_site_url(request, reverse('home'))     # Express checkout return url
            }        
            request.user.message_set.create(message='Thanks for your order!')
    except:
        transaction.rollback()
        errors = "Failed to create new invoice!"
    else:
        transaction.commit()
    #    
    view_func.context = locals()
    logger.debug('review_and_process_payment_info: session #%s: payment request for invoice [%s] submitted to paypal with item=%s, context=%s' % (
        request.session.session_key, 
        invoice,
        view_func.item,
        view_func.context)
    )
    return view_func(request)
        
