from datetime import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _

from orders.models import WorkingOrder

#global package_upload_location
#global APPSTORAGE
#
#
#
#class DesignPackage(models.Model):
#    """
#    Associates an order with deliverable design products.
#    
#    Design packages contain at least a .KIT file, and possibly a price report 
#    and a collection of images - floorplans, elevations and perspective views
#    """
#    order = models.ForeignKey(WorkingOrder, related_name='designpackage',
#        help_text=_('The order this design package was generated for.'))
#    #version = models.IntegerField('Revision Number', unique=True)
#    created = models.DateTimeField(_('Created'),
#        default=datetime.now, help_text=_('The timestamp of when this package was sent to the customer.'))
#
#
#class DesignPackageFile(models.Model):
#    '''
#    A file in design package delivered to a customer.
#    '''
#    class Const:
#        KIT, QUOTE, ARCHIVE, PERSPECTIVE, FLOORPLAN, ELEVATION= 'K', 'Q', 'A', 'P', 'F', 'E'  
#        DP_ATTACHMENT_CHOICES = ((KIT, '20/20 KIT File'), 
#                                 (QUOTE, 'Quote'), 
#                                 (ARCHIVE, 'Image Archive'), 
#                                 (PERSPECTIVE, 'Image File'),
#                                 (FLOORPLAN, 'Image File'),
#                                 (ELEVATION, 'Image File'),
#        )
#    design_package = models.ForeignKey(DesignPackage)
#    type = models.CharField(_('type'), max_length=1, choices=Const.DP_ATTACHMENT_CHOICES)
#    file = models.FileField(_('file'), upload_to=package_upload_location, storage=APPSTORAGE)
#    
