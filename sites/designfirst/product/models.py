from django.db import models

# Create your models here.

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
            
    name            = models.CharField(max_length=20)
    verbose_name    = models.CharField(max_length=120)
    description     = models.TextField()    
    sort_order      = models.IntegerField(default=100)
    base_price      = models.DecimalField(max_digits=10, decimal_places=2)
    credit_value    = models.SmallIntegerField() 
    purchaseable    = models.BooleanField(default=True)
    debitable       = models.BooleanField()
    
    class Meta:
        ordering = ('sort_order',)

    def __unicode__(self):
        return self.verbose_name
    
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
    if customer and customer.price_sheet:
        prices = customer.price_sheet.pricesheetentry_set.objects.filter(product=product)
        if prices:
            price = prices[0].retail_price
    return price
    
