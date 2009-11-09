from datetime import datetime, timedelta
import os, os.path
import logging
import urlparse

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files.base import File as DjangoFile
from django.core.files.storage import FileSystemStorage
from django.db.transaction import commit_on_success
from django.db import models
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext, ugettext_lazy as _

from utils.pdf import pdf2ppm
from utils.fields import DimensionField
from signals import status_changed

logger = logging.getLogger('orders.models')

PREVIEW_GENERATION_FAILED_IMG_FILE = os.path.join(settings.MEDIA_ROOT,'images', 'preview-failed.png')
PREVIEW_GENERATION_FAILED_IMG_SIZE = (450,600)

class AppStorage(FileSystemStorage):
    def __init__(self): 
        super(AppStorage, self).__init__(
            location=getattr(settings, 'APP_FILES_ROOT', settings.MEDIA_ROOT), 
            base_url=getattr(settings, 'APP_FILES_URL', settings.MEDIA_URL)       
        )
        
    def url(self,name):
        if not self.base_url or urlparse.urlparse(self.base_url).scheme:
            return super(AppStorage, self).url(name)
        return os.path.join(self.base_url, name)
        
APPSTORAGE = AppStorage()        
    
def attachment_upload_location(attachment_obj, filename):
    return os.path.join( 'account-data',
        str(attachment_obj.order.owner.get_profile().account.id), 
        'order-data',
        str(attachment_obj.order.id), 
        'diagrams',
        str(filename)
    )    
    
def preview_upload_location(preview_obj, filename):
    return os.path.join( 'account-data', 
        str(preview_obj.attachment.order.owner.get_profile().account.id), 
        'order-data',
        str(preview_obj.attachment.order.id), 
        'previews',
        str(filename)
    )

class WorkingOrder(models.Model):
    """
    This is a temporary object used for storing data 
    when  user goes step to step in orders
    """
    #Basic stuff
    DEALER_EDIT, SUBMITTED, ASSIGNED, COMPLETED = range(1,5) #TODO: change from number to code
    STATUS_CHOICES = (
        (DEALER_EDIT, 'Dealer Editing'),
        (SUBMITTED, 'Submitted'),
        (ASSIGNED, 'Assigned'),
        (COMPLETED, 'Completed'),
    )
    
    owner = models.ForeignKey(User)
    updated = models.DateTimeField(_('Last Updated'), auto_now=True, editable=False)
    submitted = models.DateTimeField(_('Submitted On'), null=True, blank=True, editable=False)
    status = models.PositiveSmallIntegerField(_('Status'), choices=STATUS_CHOICES, default=DEALER_EDIT)
    
    #Submit options
    project_name = models.CharField(_('Project Name'), max_length=150)
    rush = models.BooleanField(_('Rush Processing'), default=False)
    color_views = models.BooleanField(_('Include Color Perspectives'), default=False)
    elevations = models.BooleanField(_('Include Elevations'), default=False)
    quoted_cabinet_list = models.BooleanField(_('Include Cabinetry Quote'), default=False)
    desired = models.DateTimeField('Desired Delivered Date', null=True)
    cost = models.DecimalField(_('Total Design Cost'), max_digits=10, decimal_places=2, blank=True, null=True)
    client_notes = models.TextField('Notes for the Designer', null=True, blank=True)

    @property
    def expected(self):
        "Expected completion time"
        if self.submitted:
            if self.rush:
                delta = timedelta(days=1)
            else:
                delta = timedelta(days=2)
            return self.submitted + delta
        return None
            
    @property
    def flags(self):
        "Processiong flags"
        flags = []
        if self.color_views:
            flags.append('PRSNTR')
        else:
            flags.append('PRO')            
        if self.rush:
            flags.append('RUSH')
        return ', '.join(flags)


    PAINT, STAIN, NATURAL, GLAZE = ('P', 'S', 'N', 'G')
    FINISH_CHOICES = (
        (STAIN, 'Stain'), (PAINT, 'Paint'), (NATURAL, 'Natural'), (GLAZE, 'Glaze'),
    )

    MAPLE, CHERRY, ALDER, LYPTUS, BIRCH, MDF, STAINLESS, PERMAFOIL, GLASS = (
        'MAPL', 'CHER', 'ALDR', 'LYPT', 'BIRC', 'MDF', 'STEEL', 'FOIL', 'GLASS')        
    DOOR_MATERIAL_CHOICES = ( 
        (MAPLE, 'Maple'), (CHERRY, 'Cherry'), (ALDER, 'Alder'), (LYPTUS, 'Lyptus'), 
        (BIRCH, 'Birch'), (MDF, 'MDF'), (STAINLESS, 'Stainless Steel'), (PERMAFOIL, 'Permafoil'), 
        (GLASS, 'Glass'),
    )
    
    #Manufacturer page (cabinetry options)
    manufacturer    = models.CharField(_('Manufacturer'), max_length=150, blank=True, null=True)
    product_line    = models.CharField(_('Product Line'), max_length=150, blank=True, null=True)
    door_style      = models.CharField(_('Door Style'), max_length=150, blank=True, null=True)
    drawer_front_style = models.CharField(_('Drawer Front Style'), max_length=150, blank=True, null=True)
    cabinet_material= models.CharField(_('Cabinet Material'), max_length=10, blank=True, null=True, choices=DOOR_MATERIAL_CHOICES)
    finish_type     = models.CharField(_('Finish Type'), max_length=150, blank=True, null=True, choices=FINISH_CHOICES, default=FINISH_CHOICES[0][0])
    finish_color    = models.CharField(_('Paint/Stain Color'), max_length=150, blank=True, null=True) # maybe 'color'?
    finish_options  =  models.CharField(_('Finish Options'), max_length=150, blank=True, null=True)
    
        
    #Hardware page
    HANDLE_NONE, HANDLE_PULL, HANDLE_KNOB = range(3)
    HANDLE_TYPES = (
            (HANDLE_NONE, 'None / Not Specified'),
            (HANDLE_PULL, 'Pull'),
            (HANDLE_KNOB, 'Knob'))
    
    door_handle_type = models.PositiveSmallIntegerField(_('Handle Type'), choices=HANDLE_TYPES, default=HANDLE_NONE)
    door_handle_model = models.CharField(_('Model/Style'), max_length=255, null=True, blank=True)
    
    drawer_handle_type = models.PositiveSmallIntegerField(_('Handle Type'), choices=HANDLE_TYPES, default=HANDLE_NONE)
    drawer_handle_model = models.CharField(_('Model/Style'), max_length=255, null=True, blank=True)
    
    #Soffits page
    has_soffits = models.BooleanField(_('Has Soffits?'), blank=True, default=False)
    soffit_width = DimensionField(_('Width'), null=True, blank=True)
    soffit_height = DimensionField(_('Height'), null=True, blank=True)
    soffit_depth = DimensionField(_('Depth'), null=True, blank=True)
    
    
    #Dimension page
    S_NONE, S_STACKED, S_STG_HWC, S_STG_HWD, S_STG_DHWC, S_STG_HBC, S_STG_DBC = range(7)
    STYLE_CHOICES = (
        (S_NONE, _('Normal')),
        (S_STACKED, _('Stacked Wall Cabinets')),
        (S_STG_HWC, _('Staggered Depth Wall Cabinets')),
        (S_STG_DHWC, _('Staggered Depth and Height Wall Cabinets')),
        (S_STG_HBC, _('Staggered Height Base Cabinets')),
        (S_STG_DBC, _('Staggered Depth Base Cabinets')))

    STANDARD_SIZES = [12,15,18,21,24,27,30,36,42]
    dimension_style = models.PositiveSmallIntegerField(_('Cabinet Arrangements'), choices=STYLE_CHOICES, default=S_NONE)
    standard_sizes = models.BooleanField(_('Use Standard Sizes'))   
    wall_cabinet_height = DimensionField(_('Wall Cabinet Height'), null=True, blank=True)
    wall_cabinet_depth = DimensionField(_('Wall Cabinet Height'), null=True, blank=True)
    base_cabinet_height = DimensionField(_('Vanity Cabinet Height'), null=True, blank=True)
    base_cabinet_depth = DimensionField(_('Depth'), null=True, blank=True)
    vanity_cabinet_height = DimensionField(_('Vanity Cabinet Height'), null=True, blank=True)
    vanity_cabinet_depth = DimensionField(_('Depth'), null=True, blank=True)
    
    #Corder cabinet page
    CORNER_NONE, CORNER_RIGHT, CORNER_LEFT = range(3)
    BUILD_CORNER_CHOICES = (
            (CORNER_NONE, _('None')),
            (CORNER_RIGHT, _('Left Opening')),
            (CORNER_LEFT, _('Right Opening')))
    
    SHELF, LAZY_SUSAN = range(1,3)
    SHELVING_CHOICES = (
            (SHELF, _('Shelf')),
            (LAZY_SUSAN, _('Lazy Susan')))
    diagonal_corner_wall = models.PositiveSmallIntegerField(_('Diagonal Corner Wall'), choices=BUILD_CORNER_CHOICES, default=CORNER_NONE)
    diagonal_corner_wall_shelv = models.PositiveSmallIntegerField(_('Shelving Option'), choices=SHELVING_CHOICES, default=SHELF)
    diagonal_corner_base = models.PositiveSmallIntegerField(_('Diagonal Corner Base'), choices=BUILD_CORNER_CHOICES, default=CORNER_NONE)
    diagonal_corner_base_shelv = models.PositiveSmallIntegerField(_('Shelving Option'), choices=SHELVING_CHOICES, default=SHELF)
    degree90_corner_wall = models.PositiveSmallIntegerField(_('Ninety Degree Corner Wall'), choices=BUILD_CORNER_CHOICES, default=CORNER_NONE)
    degree90_corner_base = models.PositiveSmallIntegerField(_('Ninety Degree Corner Base'), choices=BUILD_CORNER_CHOICES, default=CORNER_NONE)
    degree90_corner_base_shelv = models.PositiveSmallIntegerField(_('Shelving Option'), choices=SHELVING_CHOICES, default=SHELF)
    
    #Interiors page
    slide_out_trays = models.CharField(_('Slide Out Trays'), max_length=15 )
    waste_bin = models.CharField(_('Waste Bin'), max_length=15  )
    wine_rack = models.CharField(_('Wine Rack'), max_length=15  )
    plate_rack = models.CharField(_('Plate Rack'), max_length=15  )
    appliance_garage = models.CharField(_('Appliance Garage'), max_length=15 )
    
    #Miscellaneous page
    corbels = models.BooleanField(_('Corbels') )
    brackets = models.BooleanField(_('Brackets') )
    valance = models.BooleanField(_('Valence') )
    legs_feet = models.BooleanField('Legs/Feet')
    glass_doors = models.BooleanField(_('Glass Doors'), )
    range_hood = models.BooleanField(_('Range Hood'), )
    posts = models.BooleanField(_('Posts'), )
    
    class Meta:
        verbose_name = 'order'
        verbose_name_plural = 'orders'
        
    def save(self, force_insert=False, force_update=False):
        logger.debug('saving ... %s' % self)
        changed = False
        old_status = None
        new_status = self.status
        try:
            old_status = self._base_manager.get(pk=self.id).status
            changed = new_status != old_status
        except self.DoesNotExist:
            changed = True                
        super(WorkingOrder,self).save(force_insert, force_update)
        if changed:
            status_changed.send(self, old=old_status, new=new_status)
            
        
    def __unicode__(self):
        return self.project_name
    
    def attachment_previews(self):
        "Return urls of all attachment previews"
        return [a.first_preview() for a in self.attachments.all()]
    
    
    
class Moulding(models.Model):
    TOP, BOTTOM, BASE, SCRIBE, OTHER = range(1,6)
    TYPE_CHOICES = (
        (TOP, _('Top of Wall Cabinet')),
        (BOTTOM, _('Bottom of Wall Cabinet')),
        (BASE, _('Base Cabinet')),
        (SCRIBE, _('Scribe')),
        (OTHER, _('Other')),
    )
    order = models.ForeignKey(WorkingOrder, related_name='mouldings')
    num = models.PositiveIntegerField(_('#'), )
    type = models.PositiveSmallIntegerField(_('Type'), choices=TYPE_CHOICES)
    name = models.CharField(_('Moulding Style/Model'), max_length=255)
    
    class Meta:
        ordering = [_('type'), _('num')]
    
    def __unicode__(self):
        return '#%d %s %s' % (self.num, self.get_type_display(), self.name)
    
    def save(self, *args, **kwargs):
        if self.num is None:
            self.num = self._next_num()
        super(Moulding, self).save()
    
    def delete(self):
        order, type = self.order, self.type
        super(Moulding, self).delete()
        self.reorder(order, type)
    
    def _next_num(self):
        items = list(Moulding.objects.filter(order=self.order, type=self.type))
        if len(items) == 0:
            return 1
        return items[-1].num + 1
    
    @classmethod
    def groups(cls, order):
        "Returns mouldings grouped by type"
        data = SortedDict()
        items = list(cls.objects.filter(order=order))
        for t,n in cls.TYPE_CHOICES:
            type_items = [i for i in items if i.type == t]
            if len(type_items) > 0:
                data[n] = type_items 
        return data
    
    @classmethod
    @commit_on_success
    def reorder(cls, order, type, new_sort_order=None):
        if new_sort_order is None:
            items = cls.objects.filter(order=order, type=type)
        else:
            items = [cls.objects.get(order=order, type=type, pk=i) for i in new_sort_order]
        i = 1
        for item in items:
            item.num = i
            item.save()
            i += 1
                

class Attachment(models.Model):
    FLOORPLAN, PHOTO, OTHER = range(1,4)
    TYPE_CHOICES = (
            (FLOORPLAN, _('Floorplan Sketch')),
            (PHOTO, _('Photograph')),
            (OTHER, _('Other')),)
    UPLOADED, FAXED = ('U','F')
    ATTACHMENT_SRC_CHOICES=((UPLOADED, _('Uploaded')),(FAXED, _('Faxed')),)
    
    order = models.ForeignKey(WorkingOrder, related_name='attachments')
    type = models.PositiveSmallIntegerField(_('type'), choices=TYPE_CHOICES, default=FLOORPLAN)
    file = models.FileField(_('file'), upload_to=attachment_upload_location, storage=APPSTORAGE)
    source = models.CharField(_('attachment method'), max_length=1, choices=ATTACHMENT_SRC_CHOICES, default=FAXED, editable=False)
    timestamp = models.DateTimeField(_(''), auto_now_add=True)
    
    def __unicode__(self):
        return self.file and os.path.basename(self.file.path) or '(no file)'


    @property
    def is_multipage(self):
        if self.file:
            filename = self.file.name.lower()
            return filename.endswith('.pdf') or filename.endswith('.tif') or filename.endswith('.tiff')
        return False
    
    @property
    def first_preview(self):
        if self.is_multipage:
            return self.attachpreview_set.all()[0].file.url
        return self.file and self.file.url or None
    
    @property
    def previews(self):
        if self.is_multipage:
            for f in self.attachpreview_set.count():
                yield {'url':f.file.url, 'page': f.page}
        else:
            yield {'url':self.file and self.file.url or None, 'page': 1}
    
    @property
    def page_count(self):
        if self.is_multipage:
            return self.attachpreview_set.all().count()
        return 1
    
    def generate_pdf_previews(self):
        if not self.file:
            raise RuntimeError('Attempt to generate previews for empty attachment (null file )')
        try:
            pdf2ppm(self.file.path, [(300, 600)], self._pdf_callback)
        except OSError:
            logger.error('OSError: pdf generation failed for %s' % self.file.path)
            self._pdf_callback(PREVIEW_GENERATION_FAILED_IMG_FILE, 0, PREVIEW_GENERATION_FAILED_IMG_SIZE)

    
    def _pdf_callback(self, filename, page, size):
        preview = AttachPreview(page=page, attachment=self)
        file = DjangoFile(open(filename, 'rb'))
        preview.file.save(file.name, file)
        preview.save()
        
    class Meta:
        verbose_name = _('attachment')
        verbose_name_plural = _('attachments')


class AttachPreview(models.Model):
    "Stores PDF pages converted to images"
    attachment = models.ForeignKey(Attachment)
    page = models.PositiveIntegerField(_('page'), )
    file = models.ImageField(_('file'), upload_to=preview_upload_location, storage=APPSTORAGE)
    
    class Meta:
        verbose_name = _('attachment preview')
        verbose_name_plural = _('attachment previews')
#         ordering = ['page']
    

class Appliance(models.Model):
    TYPES = ['Refrigerator', 'Microwave', 'Sink', 'Offset Sink', 'Double sink', 'Bar Sink', 'Cooktop', 'Oven', 
        'Double Oven', 'Range', 'Range Top', 'Coffee Maker', 'Under Counter Refrigerator', 'Vent Hood']
    
    order = models.ForeignKey(WorkingOrder, editable=False, related_name='appliances')
    type = models.CharField(_('Type'), max_length=20, choices=[(i,i) for i in TYPES])
    model = models.CharField(_('Model'), max_length=30, null=True, blank=True)
    width = DimensionField(_(''), null=True, blank=True)
    height = DimensionField(_(''), null=True, blank=True)
    depth = DimensionField(_(''), null=True, blank=True)
    options = models.CharField(_('Options'), max_length=80, null=True, blank=True)
    
    def __unicode__(self):
        return self.type
