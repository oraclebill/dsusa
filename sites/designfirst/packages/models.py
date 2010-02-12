from datetime import datetime
import os
import tempfile

from django.db import models
from django.utils.translation import ugettext_lazy as _

from orders.models import WorkingOrder, APPSTORAGE

#global package_upload_location
#global APPSTORAGE
#
#
#

order_storage = object()

def package_files_location(subdir=''):
    def order_package_files(instance, fname):
        # <order-store>/packages/<version>/<subdir>/file
        order = instance.order        
        order_root = order.get_file_root()
        package_id = instance.id
        assert( package_id )
        if subdir is None:
            subdir = ''
        return os.path.join(order_root, subdir, package_id, str(fname))
    return order_package_files
    
class DesignPackage(models.Model):
    """
    Associates an order with deliverable design products.
    
    Design packages contain at least a .KIT file, and possibly a price report 
    and a collection of images - floorplans, elevations and perspective views
    """    
    class Const:
        INITIAL, CORRECTION, UPDATE = 'I', 'C', 'U'
        PACKAGE_TYPES = ((INITIAL,'Initial'),(CORRECTION,'Correction'),(UPDATE,'Update'),)
        
    order = models.ForeignKey(WorkingOrder, related_name='design_packages',
        help_text=_('The order this design package was generated for.'))
    created = models.DateTimeField(_('Created'),
        default=datetime.now, help_text=_('The timestamp of when this package was sent to the customer.'))
    pkg_type = models.CharField(_('Type'), max_length=1, choices=Const.PACKAGE_TYPES, default=Const.INITIAL,
                                help_text=_('Package updates come in two forms - corrections and updates. Corrections replace, updates add.'))
    related_id = models.ForeignKey('DesignPackage', related_name='parent', limit_choices_to={ 'order': order }, null=True, blank=True )
    price_report = models.FileField(_('Price Report'), upload_to=package_files_location(), storage=order_storage)
    kitfile = models.FileField(_('Price Report'), upload_to=package_files_location(), storage=APPSTORAGE)
    frozen = models.BooleanField(_('Sealed'), default=False)
    
class DesignPackageFile(models.Model):
    '''
    A file in design package delivered to a customer.
    '''
    class Const:
        PERSPECTIVE, FLOORPLAN, ELEVATION, OTHER = 'P', 'F', 'E', 'O'  
        DP_ATTACHMENT_CHOICES = ((PERSPECTIVE, 'Color Perspective'),
                                 (FLOORPLAN, 'Floorplan'),
                                 (ELEVATION, 'Elevation'),
                                 (OTHER, 'Other'),
        )
    design_package = models.ForeignKey(DesignPackage)
    file_type = models.CharField(_('Type'), max_length=1, choices=Const.DP_ATTACHMENT_CHOICES)
    design_file = models.FileField(_('File'), upload_to=package_files_location(file_type), storage=APPSTORAGE)
    
