from django.contrib.auth.models import User
from django.db import transaction

from models import Product, CartItem
    
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

