from  uuid import uuid1 as uuid

from paypal.pro.views import PayPalPro    
        
        
from django.http import HttpResponseRedirect
# from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.contrib.auth.models import User

from product.models import Product, PriceSchedule, PriceScheduleEntry, get_customer_price, Invoice
    
def product_list(request):
    user = request.user
    if user is None or not user.is_authenticated():
        return HttpResponseRedirect('/') ## FIXME with decorators..
    
    account         = request.user.get_profile().account.dealerorganization
    pricelist       = [ (product, get_customer_price(account,product)) 
                        for product in Product.objects.filter(purchaseable=True) ]
    
    if request.method == 'POST':
        products_quantities = [ (int(id), count) for (id, count) in request.POST.itemsiter() if id.startswith('count_')]
        if product_quantities:
            for prod_id, qty in products_quantities:
                item = CartItem()
                item.session = request.session()
                item.product = Product.objects.get(pk=prod_id)
                item.quantity = qty
                item.unit_cost = product.base_cost
                item.extended_cost = item.unit_cost * qty
                item.save()
                
        products_quantities_cost = [(p,q, p*q) or (p,q) in products_quantities] 
        
    else:
        
    return render_to_response( "product/product_selection.html", 
        locals(), context_instance=RequestContext(request) )
        
def product_detail(request, prodid):
    user = request.user
    if user is None or not user.is_authenticated():
        return HttpResponseRedirect('/') ## FIXME
    
    account         = request.user.get_profile().account.dealerorganization
    product         = Product.objects.get(pk=prodid)
    price_retail    = get_customer_price(account, product)
        
    return render_to_response( "product/product_detail.html", 
        locals(), context_instance=RequestContext(request) )
    
def product_purchase(request, prodid, qty=1):
    """
    Start the purchase process.
    """    
    user = request.user
    if user is None or not user.is_authenticated():
        return HttpResponseRedirect('/')        ## FIXME
    
    account = request.user.get_profile().account.dealerorganization
        
    # get cart
    cart = Cart.objects.get(pk=prodid)
    
    # create invoice, 'pending' status
    invoice = Invoice(id=uuid().get_hex(), customer=account, status=Invoice.PENDING)
    invoice.description = "Web purchase - %s" % product.name
    invoice.add_line(
        product.name, 
        get_customer_price(account, product), 
        qty)
    invoice.save()  # default status == PENDING

    # create a paypal charge request
    item = {
        "amt":          invoice.total,
        "invnum":       invoice.id,
        "desc":         invoice.description,
        "cancelurl":    reverse(product_list),          # Express checkout cancel url
        "returnurl":    reverse('dealer-dashboard') }   # Express checkout return url            
    kw = {
        "item":             item,                       # what you're selling
        "payment_template": "paypal/payment.html",      # template name for payment
        "confirm_template": "paypal/confirmation.html", # template name for confirmation
        "success_url":      reverse('dealer-dashboard') }   # redirect location after success        
            
    ppp = PayPalPro(**kw)                
    return ppp(request)
            

def success_callback(sender, **kwargs):
    invnum = sender['invnum']    
    invoice = Invoice.objects.get(pk=invnum)
    invoice.status = Invoice.PAID
    from home.models import register_purchase
    register_purchase(invoice.id, invoice.customer, invoice.total, invoice.total_credit)
        
from paypal.pro.signals import payment_was_successful
payment_was_successful.connect(success_callback)

