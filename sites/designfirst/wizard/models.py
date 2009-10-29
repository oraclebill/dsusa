from datetime import datetime, timedelta

from django.db.transaction import commit_on_success
from django.utils.translation import ugettext, ugettext_lazy as _
import os
import logging

from utils.fields import DimensionField
from django.contrib.auth.models import User
from django.core.files.base import File as DjangoFile
from django.utils.datastructures import SortedDict
from django.db import models
from utils.pdf import pdf2ppm

import settings
PREVIEW_GENERATION_FAILED_IMG_FILE = os.path.join(settings.MEDIA_ROOT,'images', 'preview-failed.png')
PREVIEW_GENERATION_FAILED_IMG_SIZE = (450,600)

log = logging.getLogger('wizard.models')

class WorkingOrder(models.Model):
    """
    This is a temporary object used for storing data 
    when  user goes step to step in wizard
    """
    #Basic stuff
    DEALER_EDIT, SUBMITTED, ASSIGNED = range(1,4)
    STATUS_CHOICES = (
        (DEALER_EDIT, 'Dealer Editing'),
        (SUBMITTED, 'Submitted'),
        (ASSIGNED, 'Assigned'),
    )
    
    owner = models.ForeignKey(User)
    updated = models.DateTimeField(_('Last Updated'), auto_now=True, editable=False)
    submitted = models.DateTimeField(_('Submitted On'), auto_now=False, editable=False)
    status = models.PositiveSmallIntegerField(_('Status'), choices=STATUS_CHOICES, default=DEALER_EDIT)
    
    #Submit options
    project_name = models.CharField(_('Project Name'), max_length=150)
    rush = models.BooleanField(_('Rush Processing'), default=False)
    color_views = models.BooleanField(_('Include Color Perspectives'), default=False)
    elevations = models.BooleanField(_('Include Elevations'), default=False)
    quoted_cabinet_list = models.BooleanField(_('Include Cabinetry Quote'), default=False)
    desired = models.DateTimeField('Desired Delivered Date')
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
    has_soffits = models.NullBooleanField(_('Has Soffits?'), null=True, blank=True)
    soffit_width = DimensionField(_('Width'), null=True, blank=True)
    soffit_height = DimensionField(_('Height'), null=True, blank=True)
    soffit_depth = DimensionField(_('Depth'), null=True, blank=True)
    
    
    #Dimension page
    S_NONE, S_STACKED, S_STG_HWC, S_STG_DHWC, S_STG_HBC, S_STG_DBC = range(6)
    STYLE_CHOICES = (
        (S_NONE, _('Normal')),
        (S_STACKED, _('Stacked Wall Cabinets')),
        (S_STG_HWC, _('Staggered Height Wall Cabinets')),
        (S_STG_DHWC, _('Staggered Depth and Height Wall Cabinets')),
        (S_STG_HBC, _('Staggered Height Base Cabinets')),
        (S_STG_DBC, _('Staggered Depth Base Cabinets')))

    STANDARD_SIZES = [16, 32, 36]
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
    slide_out_trays = models.BooleanField(_('Slide Out Trays') )
    waste_bin = models.BooleanField(_('Waste Bin') )
    wine_rack = models.BooleanField(_('Wine Rack') )
    plate_rack = models.BooleanField(_('Plate Rack') )
    appliance_garage = models.BooleanField(_('Appliance Garage') )
    
    #Miscellaneous page
    corbels = models.BooleanField(_('Corbels') )
    brackets = models.BooleanField(_('Brackets') )
    valance = models.BooleanField(_('Valence') )
    legs_feet = models.BooleanField('Legs/Feet')
    glass_doors = models.BooleanField(_('Glass Doors'), )
    range_hood = models.BooleanField(_('Range Hood'), )
    posts = models.BooleanField(_('Posts'), )
    
    def __unicode__(self):
        return self.project_name
    
    def attachement_previews(self):
        "Return urls of all attachment previews"
        return [a.first_preview() for a in self.attachments.all()]
    
    
    
class Moulding(models.Model):
    TOP, BASE, BOTTOM = range(1,4)
    TYPE_CHOICES = (
        (TOP, _('Top of Wall Cabinet')),
        (BOTTOM, _('Bottom of Wall Cabinet')),
        (BASE, _('Base Cabinet')),
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
    ATTACHMENT_SRC_CHOICES=((UPLOADED, _('Upload')),(FAXED, _('Faxed')),)
    
    order = models.ForeignKey(WorkingOrder, related_name='attachments')
    type = models.PositiveSmallIntegerField(_('Type'), choices=TYPE_CHOICES)
    file = models.FileField(_('File'), upload_to='data/wizard/attachments/%Y/%m')
    source = models.CharField(_('Source'), max_length=1, choices=ATTACHMENT_SRC_CHOICES, default=UPLOADED, editable=False)
    timestamp = models.DateTimeField(_(''), auto_now_add=True)
    
    def __unicode__(self):
        return os.path.basename(self.file.path)
    
    def first_preview(self):
        if self.is_pdf():
            return self.attachpreview_set.all()[0].file.url
        return self.file.url
    
    def previews(self):
        if self.is_pdf():
            for f in self.attachpreview_set.all():
                yield {'url':f.file.url, 'page': f.page}
        else:
            yield {'url':self.file.url, 'page': 1}
    
    def page_count(self):
        if self.is_pdf():
            return self.attachpreview_set.all().count()
        return 1
    
    def is_pdf(self):
        return self.file.name.lower().endswith('.pdf')
    
    def generate_pdf_previews(self):
        try:
            pdf2ppm(self.file.path, [(300, 600)], self._pdf_callback)
        except OSError:
            log.error('OSError: pdf generation failed for %s' % self.file.path)
            self._pdf_callback(PREVIEW_GENERATION_FAILED_IMG_FILE, 0, PREVIEW_GENERATION_FAILED_IMG_SIZE)

    
    def _pdf_callback(self, filename, page, size):
        preview = AttachPreview(page=page, attachment=self)
        file = DjangoFile(open(filename, 'rb'))
        preview.file.save(file.name, file)
        preview.save()


class AttachPreview(models.Model):
    "Stores PDF pages converted to images"
    attachment = models.ForeignKey(Attachment)
    page = models.PositiveIntegerField(_(''), )
    file = models.ImageField(_(''), upload_to='data/wizard/attachments/%Y/%m/preview')
    
    class Meta:
        ordering = ['page']
    

class Appliance(models.Model):
    TYPES = ['Refrigerator', 'Microwave', 'Double sink', 'Cooktop','Oven']
    
    order = models.ForeignKey(WorkingOrder, editable=False, related_name='appliances')
    type = models.CharField(_('Type'), max_length=20, choices=[(i,i) for i in TYPES])
    model = models.CharField(_('Model'), max_length=30, null=True, blank=True)
    width = DimensionField(_(''), null=True, blank=True)
    height = DimensionField(_(''), null=True, blank=True)
    depth = DimensionField(_(''), null=True, blank=True)
    options = models.CharField(_('Options'), max_length=80, null=True, blank=True)
    
    def __unicode__(self):
        return self.type
