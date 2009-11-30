from datetime import datetime
from hashlib import sha1
import logging

from django.contrib.auth.models import User
from django.db import transaction

from customer.models import Invoice
from models import Product, CartItem

logger = logging.getLogger('product.cart')

@transaction.commit_on_success
def new_cart(request, product_ids=[]):
    """
    Initiate a purchase using the selected product and processing options.
    """    
    assert(len(product_ids))
    CartItem.objects.filter(session_key=request.session.session_key).delete()   
    item_count = 1
    for prodid in product_ids: 
        item = CartItem(
            number = item_count,
            session_key = request.session.session_key,
            product = Product.objects.get(pk=prodid),
            quantity = 1
        )
        item.save()
        item_count += 1

@transaction.commit_on_success
def add_item(cart_id, item_id, quantity):
    assert(cart_id)
    item_count = CartItem.objects.filter(session_key=cart_id).count()
    item = CartItem.objects.create(session_key=cart_id,
                            number=item_count+1, 
                            product_id=item_id,
                            quantity=quantity)
    item.save()

@transaction.commit_on_success
def destroy_cart(cart):
    items = CartItem.objects.filter(session_key=cart).delete()
        
                
def get_cart_from_request(request):
    assert(request.user.is_authenticated())
    return request.session.session_key

def get_cart_items(cart):
    return CartItem.objects.filter(session_key=cart)

@transaction.commit_on_success
def create_invoice_from_cart(cart, account, user):
    logger.debug('create_invoice_from_cart: entering: cart=%s, account=%s, user=%s', cart, account, user)
    
    sig = sha1(repr(datetime.now())).hexdigest()
    invoice = Invoice(id=sig, customer=account, status=Invoice.Const.NEW)
    cart_items = get_cart_items(cart)    
    
    items = []
    for item in cart_items:
        logger.debug('create_invoice_from_cart: adding invoice line: item=%s', item)
        invoice.add_line(item.product.name, item.product.base_price, item.quantity)
        items.append(item.product.name)
        item.delete()

    invoice.description = " $%3.02f items - %s" % (invoice.total, ', '.join(items))        
    invoice.save()       
    destroy_cart(cart) 

    return invoice
