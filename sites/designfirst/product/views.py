from uuid import uuid1 as uuid
from datetime import datetime
from decimal import Decimal
from hashlib import sha1
from pickle import dumps

from paypal.pro.views import PayPalPro            

from django.db import transaction
from django.db.models import Sum        
from django.http import HttpResponseRedirect
# from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.contrib.auth.models import User

from accounting.models import register_purchase
from models import Product, PriceSchedule, PriceScheduleEntry, get_customer_price 
from models import Invoice, CartItem
    
def make_site_url(request, path):
    from django.contrib.sites.models import Site
    scheme = request.is_secure() and 'https' or 'http'
    domain = Site.objects.get_current().domain
    return '%s://%s/%s' % (scheme, domain, path)
    
def product_detail(request, prodid):
    user = request.user
    if user is None or not user.is_authenticated():
        return HttpResponseRedirect('/') ## FIXME
    
    account         = request.user.get_profile().account
    product         = Product.objects.get(pk=prodid)
    price_retail    = get_customer_price(account, product)
        
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
                # item.unit_price = get_customer_price(account, product)
                item.save()
                
        if '_purchase' in request.POST:            
            if cart_empty:
                errors = ["You cannot checkout until you purchase at least one item!"]
            else:
                # go to confirmation page
                return HttpResponseRedirect(reverse("confirm_purchase_selections"))

    # using a aggregate here seems silly, but baffled as to how else to do this cleanly..
    pricelist = [ ( product, 
                    get_customer_price(account,product), 
                    product.cartitem_set.aggregate(Sum('quantity')).get('quantity__sum') or 0
                  ) for product in Product.objects.filter(purchaseable=True) ]
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
    account = request.user.get_profile().account
    cart_items = CartItem.objects.filter(session_key__exact=request.session.session_key)    
    # if the cart is empty we have nothing to do..
    if not cart_items:
        return HttpResponseRedirect('/invoices') ##TODO- fix        
    cart_total = sum([i.extended_price for i in cart_items])
    view_func = PayPalPro(payment_template="product/payment_info_review.html",     
                    confirm_template="paypal/express_confirmation.html",
                    success_url=reverse('dealer-dashboard')
    )                
    if request.method == "POST" or (request.method == "GET" and 'express' in request.GET):        
        # get a signature for this cart so we can tie it uniquely to our invoice
        sig = sha1(dumps(cart_items)).hexdigest()
        # if this invoice exists, something bad happened..        
        try:
            old_invoice = Invoice.objects.get(id__exact=sig)            
            if old_invoice.status == Invoice.PENDING:
                # they're resubmitting a pending order, ignore it but log it...
                # TODO: log   
                return HttpResponseRedirect(reverse('dealer-dashboard'))    # TODO - 'success' URL         
            elif old_invoice.status == Invoice.PAID:
                # they're resubmitting a PAID order which should absolutely not be possible, bail hard..
                raise RuntimeError('PAID RESUB')
            elif old_invoice.status == Invoice.CANCELLED:
                # they're resubmitting a CANCELLED order which should absolutely not be possible, bail hard..
                raise RuntimeError('CNCL RESUB')
        except Invoice.DoesNotExist: 
            pass
            
        # also, there shouldn't be any other existing, pending invoices for this account, but lets check...
        pending_invoices = Invoice.objects.filter(customer=account, status=Invoice.PENDING)
        if pending_invoices:
            raise RuntimeError(repr(pending_invoices)) # fixme
            
        # now we know what to do.. note that none of the db operations commit unless paypal has no error (exceptions)
        invoice = Invoice(id=sig, customer=account, status=Invoice.PENDING)
        invoice.description = "Web Purchase by '%s' on '%s'" % (request.user.email, datetime.now())
        for item in cart_items:
            invoice.add_line(item.product.name, get_customer_price(account, item.product), item.quantity)
            item.delete()
        invoice.save()    
            
        # configure the paypal processor with invoice info.
        view_func.item = {
            "amt":          invoice.total,
            "invnum":       invoice.id,
            "custom":       request.session.session_key,    # for debugging
            "desc":         invoice.description,
            "cancelurl":    make_site_url(request, reverse('select_products')),     # Express checkout cancel url
            "returnurl":    make_site_url(request, reverse('dealer-dashboard'))    # Express checkout return url
        }
        view_func.context = locals()
    return view_func(request)
        
@transaction.commit_on_success
def paypal_success_callback(sender, **kwargs):
    invnum = sender['invnum']    
    invoice = Invoice.objects.get(pk=invnum)
    invoice.status = Invoice.PAID
    invoice.save()
    register_purchase(invoice.id, invoice.customer, invoice.total, invoice.total_credit)
        
from paypal.pro.signals import payment_was_successful
payment_was_successful.connect(paypal_success_callback)

