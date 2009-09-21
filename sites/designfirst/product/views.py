
from django.http import HttpResponseRedirect
# from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.template import RequestContext
from django.shortcuts import render_to_response

from django.contrib.auth.models import User

from product.models import Product, PriceSchedule, PriceScheduleEntry, get_customer_price
    
def product_list(request):
    user = request.user
    if user is None or not user.is_authenticated():
        return HttpResponseRedirect('/') ## FIXME with decorators..
    
    account         = request.user.get_profile().account.dealeraccount
    pricelist       = [ (product, get_customer_price(account,product)) 
                        for product in Product.objects.filter(purchaseable=True) ]
        
    return render_to_response( "product/product_list.html", 
        locals(), context_instance=RequestContext(request) )
        
def product_detail(request, prodid):
    user = request.user
    if user is None or not user.is_authenticated():
        return HttpResponseRedirect('/') ## FIXME
    
    account         = request.user.get_profile().account.dealeraccount
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
    
    account = request.user.get_profile().account.dealeraccount
        
    # get product and price information
    product         = Product.objects.get(pk=prodid)
    price_retail    = get_customer_price(account, product) * qty

    # create a paypal charge request
    item = {
        "amt":          price_retail,
        "invnum":       product.id,
        "desc":         product.name,
        "cancelurl":    reverse(product_list),          # Express checkout cancel url
        "returnurl":    reverse('dealer-dashboard') }   # Express checkout return url            
    kw = {
        "item":             item,                       # what you're selling
        "payment_template": "paypal/payment.html",      # template name for payment
        "confirm_template": "paypal/confirmation.html", # template name for confirmation
        "success_url":      reverse('dealer-dashboard') }            # redirect location after success        

    from paypal.pro.views import PayPalPro    
    ppp = PayPalPro(**kw)                
    return ppp(request)
            
