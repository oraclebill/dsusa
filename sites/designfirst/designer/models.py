from django.utils.translation import ugettext as _
from django.db import models
from home.models import Organization, DesignOrder

# Create your models here.

class DesignOrganization(Organization):
    """
    A profile object for users that participate as designers.     
    """
    is_manager = models.BooleanField(_('Admin Status?'), default=False)
    # order_history = models.ManyToManyField(DesignOrder, through='DesignerOrderHistory')
    
# class Designer(models.Model):
#     """
#     """
#     name = models.CharField(_('Designer Name'), max_length=32)
#     email = models.EmailField(_('Email Address'), max_length=32)
#     
# class OrderAssignment(models.Model):    
#     designer=models.ForeignKeyField(Designer)
#     assignment=models.ForeighKeyField(DesignOrder)
#     start_date=models.DateTimeField(_('Started On'), auto_now_add=True)
#     end_date=models.DateTimeField(_('Completed On'), null=True)
#     notes=models.TextField(_('Assignment Notes'), null=True, blank=True)
#     
