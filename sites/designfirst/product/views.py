from  uuid import uuid1 as uuid
from datetime import datetime
from decimal import Decimal

from paypal.pro.views import PayPalPro            

from django.db.models import Sum        
from django.http import HttpResponseRedirect
# from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.contrib.auth.models import User

from product.models import Product, PriceSchedule, PriceScheduleEntry, get_customer_price 
from product.models import Invoice, CartItem
    
def product_detail(request, prodid):
    user = request.user
    if user is None or not user.is_authenticated():
        return HttpResponseRedirect('/') ## FIXME
    
    account         = request.user.get_profile().account.dealerorganization
    product         = Product.objects.get(pk=prodid)
    price_retail    = get_customer_price(account, product)
        
    return render_to_response( "product/product_detail.html", 
        locals(), context_instance=RequestContext(request) )
    
def select_products(request, template):
    "Display the product list and collect product id's for users purchase."
    user = request.user
    if user is None or not user.is_authenticated():
        return HttpResponseRedirect('/') ## FIXME with decorators..
    
    account = request.user.get_profile().account.dealerorganization
            
    # using a aggregate here seems silly, but baffled as to how else to do this cleanly..
    pricelist = [ ( product, 
                    get_customer_price(account,product), 
                    product.cartitem_set.aggregate(Sum('quantity')).get('quantity__sum', 0)
                  ) for product in Product.objects.filter(purchaseable=True) ]
    
    # post means they've selected somethign to purchase. put the items in your 'cart' and go to confirm stage
    if request.method == 'POST':
        CartItem.objects.all().delete()
        product_quantities = [ (int(id[6:]), count) for (id, count) in request.POST.items() if id.startswith('count_') and count]
        if product_quantities:
            
            for prod_id, qty in product_quantities:
                item = CartItem()
                item.session_key = request.session.session_key
                item.product = Product.objects.get(pk=prod_id)
                item.quantity = int(qty)
                # item.unit_price = get_customer_price(account, product)
                item.save()
        if '_purchase' in request.POST:            
            # go to confirmation page
            return HttpResponseRedirect(reverse("confirm_purchase_selections"))

    cart_items = CartItem.objects.filter(session_key__exact=request.session.session_key)
    cart_total = sum([i.extended_price for i in cart_items])
        
    return render_to_response( template, locals(), context_instance=RequestContext(request) )
                
def confirm_selections(request):
    "Display the selected products and pricing info and identify payment mechanism."
    account = request.user.get_profile().account.dealerorganization

    cart_items = CartItem.objects.filter(session_key__exact=request.session.session_key)
    cart_total = sum([i.extended_price for i in cart_items])
              
    return render_to_response( "product/product_selection_review.html", locals(), 
        context_instance=RequestContext(request) )
    
def review_and_process_payment_info(request):
    "Display and/or collect payment information while displaying a summary of products to be purchased."    
    account = request.user.get_profile().account.dealerorganization
    cart_items = CartItem.objects.filter(session_key__exact=request.session.session_key)
    cart_total = sum([i.extended_price for i in cart_items])
    view_func = PayPalPro(payment_template="product/payment_info_review.html",     
                    confirm_template="paypal/express_confirmation.html",
                    success_url=reverse('dealer-dashboard')
    )                
    if request.method == "POST":
        # get or create a pending invoice and start the paypal process
        invoice, created = Invoice.objects.get_or_create(customer=account, status=Invoice.PENDING)
        # don't bother trying to reuse old invoices..
        if not created:
            invoice.status = Invoice.CANCELLED
            invoice = Invoice(customer=account, status=Invoice.PENDING)
        # populate the invoice with cart info and save
        invoice.description = "Web Purchase by '%s' on '%s'" % (request.user.email, datetime.now())
        for item in cart_items:
            invoice.add_line(item.product.name, get_customer_price(account, item.product), item.quantity)
        invoice.save()        
        # configure the paypal processor with invoice info.
        view_func.item = {
            "amt":          invoice.total,
            "invnum":       invoice.id,
            "custom":       request.session.session_key,
            "desc":         invoice.description,
            "cancelurl":    reverse('select_products'),       # Express checkout cancel url
            "returnurl":    reverse('dealer-dashboard') }   # Express checkout return url
                        
    return view_func(request, context=locals())
        
def paypal_success_callback(sender, **kwargs):
    invnum = sender['invnum']    
    invoice = Invoice.objects.get(pk=invnum)
    invoice.status = Invoice.PAID
    from home.models import register_purchase
    register_purchase(invoice.id, invoice.customer, invoice.total, invoice.total_credit)
        
from paypal.pro.signals import payment_was_successful
payment_was_successful.connect(paypal_success_callback)

