from decimal import Decimal
from uuid import uuid1

from django.contrib.sessions.models import Session
from django.db import models
from django.utils.translation import ugettext as _

from customer.models import DealerOrganization

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
    
    def customer_price(self, customer):
        return get_customer_price(customer, self)
    
        
class PriceSchedule(models.Model):
    """
    A set of prices that apply to a group of customers.
    
    Price sheet prices override base prices.
    """
    name            = models.CharField(max_length=20)
    description     = models.TextField()
    is_default      = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.name

class PriceScheduleEntry(models.Model):
    """
    A retail price override association for a specific product/pricesheet pair
    
    """
    price_sheet     = models.ForeignKey(PriceSchedule)
    product         = models.ForeignKey(Product)
    retail_price    = models.DecimalField(max_digits=10, decimal_places=2)

    # class Meta:
    #     order_with_respect_to = 'product'

    def __unicode__(self):
        return self.product.name


def get_customer_price(customer, product):
    price = product.base_price
#     if customer and customer.price_sheet:
#         prices = customer.price_sheet.pricesheetentry_set.objects.filter(product=product)
#         if prices:
#             price = prices[0].retail_price
    return price
    
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
            
def uuid_key():
    return uuid1().hex
        
class Invoice(models.Model):
#     invoice = Invoice(id='test=1', customer=account, status=Invoice.PENDING)
#     invoice.description = "Quick Buy web purchase - %s" % product.name
#     invoice.add_line(
#         product.name, 
#         get_customer_price(account, product), 
#         qty)
#     invoice.save()  # default status == PENDING
    CANCELLED, PENDING, PAID = ('C', 'E', 'A')
    INV_STATUS_CHOICES = ((PENDING, _('PENDING')), (PAID, _('PAID')), (CANCELLED, _('CANCELLED')))

    id          = models.CharField(max_length=50, primary_key=True, default=uuid_key)
    customer    = models.ForeignKey(DealerOrganization)
    status      = models.CharField(max_length=1, choices=INV_STATUS_CHOICES)
    description = models.TextField(blank=True)
    created     = models.DateTimeField(auto_now_add=True)
    ## TODO
    # updated = models.DateTimeField(auto_now=True)
    
    @property
    def total(self):
        return reduce(
            lambda x,y: x+y, 
            [il.line_price for il in self.invoiceline_set.all()], 
            Decimal() )
    
    @property
    def total_credit(self):
        return reduce(
            lambda x,y: x+y, 
            [il.line_credit for il in self.invoiceline_set.all()], 
            Decimal() )
    
    def add_line(self, description, price, quantity=1):
        return self.invoiceline_set.create(
            description=description, 
            unit_price=price, 
            quantity=quantity
        )
        
    def __unicode__(self):
        return 'Invoice[id=%s,customer=%s,status=%s,created=%s]' % (
                    self.id or 'None', 
                    self.customer or 'None', 
                    self.status or 'None', 
                    self.created or 'None')

    
        
class InvoiceLine(models.Model):
    invoice     = models.ForeignKey(Invoice)
    number      = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=80)
    quantity    = models.IntegerField()
    unit_price  = models.DecimalField(max_digits=10, decimal_places=2)
    _unit_credit  = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    @property
    def unit_credit(self):
        return self._unit_credit or self.unit_price

    @property
    def line_price(self):
        return self.unit_price * self.quantity        
        
    @property
    def line_credit(self):
        return self.unit_credit * self.quantity        
        
