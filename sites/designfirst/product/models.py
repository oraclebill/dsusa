from decimal import Decimal
from uuid import uuid1

from django.contrib.sessions.models import Session
from django.db import models
from django.utils.translation import ugettext_lazy as _


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
    class Const:
        SUBSCRIPTION, BASE, PACKAGE, OPTION = 'S', 'B', 'P', 'O'
        PRODUCT_TYPE_CHOICES = zip([SUBSCRIPTION, BASE, PACKAGE, OPTION, BASE+PACKAGE, OPTION+PACKAGE], 
                                   ['Subscription', 'Base', 'Package', 'Option', 'Base Package', 'Option Package'])
                    
    name            = models.CharField(_('name'), max_length=120)
    description     = models.TextField(_('description'))    
    product_type    = models.CharField(_('type'), max_length=2, choices=Const.PRODUCT_TYPE_CHOICES, default=Const.BASE)
    base_price      = models.DecimalField(_('price'), max_digits=10, decimal_places=2)
    credit_value    = models.SmallIntegerField(_('credit amount') ) 
    
    class Meta:
        ordering = ('product_type', 'base_price')

    def __unicode__(self):
        return self.name

class ProductRelationship(models.Model):
    """
    Provides a way to express simple relationships between products
    """
    class Const:
        REQUIRES, COMPOSED_OF, EXCLUDES = 'R', 'C', 'E'
        DEPENDENCY_CHOICES = zip([REQUIRES, COMPOSED_OF, EXCLUDES], ['requires', 'composed of', 'not valid with']) 
           
    source = models.ForeignKey(Product, related_name='source_set', verbose_name='dependency source')
    target = models.ForeignKey(Product, related_name='target_set', verbose_name='dependency target')
    deptype = models.CharField(_('dependency type'), max_length=1, choices=Const.DEPENDENCY_CHOICES,default=Const.REQUIRES)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        unique_together = [('source', 'target', 'deptype'), ]
    
    
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
            
