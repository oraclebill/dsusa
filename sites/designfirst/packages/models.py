from datetime import datetime
import os
import uuid
import tempfile

from django.db import models
from django.utils.translation import ugettext_lazy as _

from orders.models import WorkingOrder, APPSTORAGE

def package_files_location(pkg_subdir=''):
    if pkg_subdir:
        subdir = [pkg_subdir]
    else:
        subdir = ['']
        
    def order_package_files(instance, fname):
        # <order-store>/packages/<version>/<subdir>/file
        try:
            package_id = instance.tag
        except:
            package_id = instance.design_package.tag
        assert( package_id )
        return os.path.join('design-packs', subdir[0], package_id, str(fname))
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
        
    tag = models.CharField(max_length=40, default=lambda: str(uuid.uuid1()) )
    order = models.ForeignKey(WorkingOrder, related_name='design_packages',
        help_text=_('The order this design package was generated for.'))
    designer = models.CharField(_('Designer'), max_length=30)
    kitfile = models.FileField(_('20/20 KIT File'), upload_to=package_files_location(), storage=APPSTORAGE)
    quotefile = models.FileField(_('Price Report'), upload_to=package_files_location(), storage=APPSTORAGE, null=True)
    notes = models.TextField(_('Designers Notes'), null=True, blank=True)

    sealed = models.DateTimeField(_('Sealed'), null=True, blank=True,
        default=datetime.now, help_text=_('The timestamp of when this package was sent to the customer, or null if still unsent.'))
        
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
    design_package = models.ForeignKey(DesignPackage, related_name='presentation_files')
    file_type = models.CharField(_('Type'), max_length=1, choices=Const.DP_ATTACHMENT_CHOICES)
    design_file = models.FileField(_('File'), upload_to=package_files_location('views'), storage=APPSTORAGE)
    
