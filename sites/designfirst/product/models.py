from decimal import Decimal
from uuid import uuid1

from django.contrib.sessions.models import Session
from django.db import models
from django.utils.translation import ugettext as _


DECIMAL_ZERO = Decimal()

#
# Models
#
class Product(models.Model):    
    """
    Anything that increases or decreases a customers account credit is a product. 
    
    Users purchase products which deposit credits into their accounts. They then use these
    credits to order design services, where various types of services requires differing
    amounts of credits. So in a sense there are two types of products - products that are purchased
    to increase account credit, and products that are associated with orders that decrease 
    account credit. 
    
    Product examples:
    
        standard design
        standard design with views and elevations
        standard design with views, elevations and cabinetry price report
        
        revisable design w/1 revision
        revisable design (+1 rev) with views and elevations
        revisable design (+1 rev) with views, elevations and cabinetry price report
        
        additional revision w/o views and elevations
        additional revision w/views and elevations
       
        Package: 5 Standard Designs
        Package: 5 Standard Designs w/views and elevations
        Package: 5 Standard Designs w/views, elevations and cabinetry price report

        Package: 10 Standard Designs
        Package: 10 Standard Designs w/views and elevations
        Package: 10 Standard Designs w/views, elevations and cabinetry price report
    """
    
    PRODUCT_TYPES = enumerate(('Base Product', 'Package Product', 'Option Product'))
            
    name            = models.CharField(max_length=120)
    description     = models.TextField()    
    sort_order      = models.IntegerField(default=100)
    base_price      = models.DecimalField(max_digits=10, decimal_places=2)
    credit_value    = models.SmallIntegerField() 
    purchaseable    = models.BooleanField(default=True)
    debitable       = models.BooleanField()
    is_revision     = models.NullBooleanField(null=True)
    
    class Meta:
        ordering = ('sort_order',)

    def __unicode__(self):
        return self.name
    
    
class CartItem(models.Model):    
    session_key     = models.CharField(max_length=40)
    product         = models.ForeignKey(Product)
    quantity        = models.IntegerField()

    @property
    def extended_price(self):
        if not (self.unit_price or self.quantity):
            return Decimal(0)            
        return self.quantity * self.unit_price
    
    @property
    def unit_price(self):
        if not self.product:
            return DECIMAL_ZERO
        ## TODO: how to reconcile this with account specific pricing??
        return self.product.base_price;

    def __unicode__(self):
        return 'CartItem[key=%s,product=%s,quantity=%s]' % (self.session_key or 'None', self.product and self.product.name or 'None', self.quantity or 'None')
            
