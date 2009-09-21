from django.db import models

from home.models import Account, DesignOrder

# Create your models here.

class DesignerAccount(Account):
    """
    A profile object for users that participate as designers. 
    
    
    """
    is_manager = models.BooleanField(default=False)
    # order_history = models.ManyToManyField(DesignOrder, through='DesignerOrderHistory')
    
    def __unicode__(self):
        return 'Designer: %s' % self.id
    
    
# class DesignerOrderHistory(models.Model):
#     """
#     A log of orders associated with a designer.
#     
#     
#     """
#     designer = models.ForeignKey(DesignerAccount)
#     order = models.ForeignKey(DesignOrder)
#     date_assigned = models.DateField()
#     date_completed = models.DateField()
#     had_designer_issues = models.BooleanField()
#     had_client_issues = models.BooleanField()