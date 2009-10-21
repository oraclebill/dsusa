from django.db.transaction import commit_on_success
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
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=DEALER_EDIT)
    #Submit options
    color_views = models.BooleanField(default=False)
    elevations = models.BooleanField(default=False)
    quoted_cabinet_list = models.BooleanField(default=False)

    
    
    #New page
    project_name = models.CharField(max_length=150)
    desired = models.DateTimeField('Desired Completion')
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    client_notes = models.TextField('Notes', null=True, blank=True)
    
    #Manufacturer page (cabinetry options)
    cabinet_manufacturer = models.CharField(max_length=150, blank=True, null=True, 
        verbose_name='Manufacturer')
    cabinet_product_line = models.CharField(max_length=150, blank=True, null=True, 
        verbose_name='Product Line')
    cabinet_door_style = models.CharField(max_length=150, blank=True, null=True, 
        verbose_name='Door Style')
    cabinet_wood = models.CharField(max_length=150, blank=True, null=True, 
        verbose_name='Wood')
    cabinet_finish = models.CharField(max_length=150, blank=True, null=True, 
        verbose_name='Finish')
    cabinet_finish_options =  models.CharField(max_length=150, blank=True, null=True, 
        verbose_name='Special Options')
    cabinetry_notes =  models.TextField('Notes', null=True, blank=True)
    
    
    #Hardware page
    HANDLE_NONE, HANDLE_PULL, HANDLE_KNOB = range(3)
    HANDLE_TYPES = (
            (HANDLE_NONE, 'None / Not Specified'),
            (HANDLE_PULL, 'Pull'),
            (HANDLE_KNOB, 'Knob'))
    
    door_handle_type = models.PositiveSmallIntegerField(choices=HANDLE_TYPES, default=HANDLE_NONE)
    door_handle_model = models.CharField(max_length=255, null=True, blank=True)
    
    drawer_handle_type = models.PositiveSmallIntegerField(choices=HANDLE_TYPES, default=HANDLE_NONE)
    drawer_handle_model = models.CharField(max_length=255, null=True, blank=True)
    
    #Soffits page
    soffit_width = DimensionField('Width', null=True, blank=True)
    soffit_height = DimensionField('Height', null=True, blank=True)
    soffit_depth = DimensionField('Depth', null=True, blank=True)
    
    
    #Dimension page
    S_NONE, S_STACKED, S_STG_HWC, S_STG_DHWC, S_STG_HBC, S_STG_DBC = range(6)
    STYLE_CHOICES = (
        (S_NONE, 'None'),
        (S_STACKED, 'Stacked Wall Cabinets'),
        (S_STG_HWC, 'Staggered Height Wall Cabinets'),
        (S_STG_DHWC, 'Staggered Depth and Height Wall Cabinets'),
        (S_STG_HBC, 'Staggered Height Base Cabinets'),
        (S_STG_DBC, 'Staggered Depth Base Cabinets'))

    STANDARD_SIZES = [16, 32, 36]
    dimension_style = models.PositiveSmallIntegerField(choices=STYLE_CHOICES, default=S_NONE)
    standard_sizes = models.BooleanField('Standard sizes')   
    wall_cabinet_height = DimensionField(null=True, blank=True)
    vanity_cabinet_height = DimensionField(null=True, blank=True)
    depth = DimensionField(null=True, blank=True)
    
    #Corder cabinet page
    CORNER_NONE, CORNER_RIGHT, CORNER_LEFT = range(3)
    BUILD_CORNER_CHOICES = (
            (CORNER_NONE, 'None'),
            (CORNER_RIGHT, 'Left Opening'),
            (CORNER_LEFT, 'Right Opening'))
    
    SHELF, LAZY_SUSAN = range(1,3)
    SHELVING_CHOICES = (
            (SHELF, 'Shelf'),
            (LAZY_SUSAN, 'Lazy Susan'))
    diagonal_corner_base = models.PositiveSmallIntegerField(choices=BUILD_CORNER_CHOICES, default=CORNER_NONE)
    diagonal_corner_base_shelv = models.PositiveSmallIntegerField(choices=SHELVING_CHOICES, default=SHELF)
    diagonal_corner_wall = models.PositiveSmallIntegerField(choices=BUILD_CORNER_CHOICES, default=CORNER_NONE)
    diagonal_corner_wall_shelv = models.PositiveSmallIntegerField(choices=SHELVING_CHOICES, default=SHELF)
    degree90_corner_base = models.PositiveSmallIntegerField(choices=BUILD_CORNER_CHOICES, default=CORNER_NONE)
    degree90_corner_base_shelv = models.PositiveSmallIntegerField(choices=SHELVING_CHOICES, default=SHELF)
    degree90_corner_wall = models.PositiveSmallIntegerField(choices=BUILD_CORNER_CHOICES, default=CORNER_NONE)
    
    #Interiors page
    lazy_susan = models.BooleanField()
    slide_out_trays = models.BooleanField()
    waste_bin = models.BooleanField()
    wine_rack = models.BooleanField()
    plate_rack = models.BooleanField()
    apliance_garage = models.BooleanField()
    
    #Miscellaneous page
    corables = models.BooleanField()
    brackets = models.BooleanField()
    valance = models.BooleanField()
    leas_feet = models.BooleanField('Leas/Feet')
    glass_doors = models.BooleanField()
    range_hood = models.BooleanField()
    posts = models.BooleanField()
    
    def __unicode__(self):
        return self.project_name
    
    def attachement_previews(self):
        "Return urls of all attachment previews"
        return [a.first_preview() for a in self.attachments.all()]
    
    
class Attachment(models.Model):
    FLOORPLAN, PHOTO, OTHER = range(1,4)
    TYPE_CHOICES = (
            (FLOORPLAN, 'Floorplan Sketch'),
            (PHOTO, 'Photograph'),
            (OTHER, 'Other'),)
    order = models.ForeignKey(WorkingOrder, related_name='attachments')
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    file = models.FileField(upload_to='data/wizard/attachments/%Y/%m')
    timestamp = models.DateTimeField(auto_now_add=True)
    
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


class Moulding(models.Model):
    TOP, BASE, BOTTOM = range(1,4)
    TYPE_CHOICES = (
        (TOP, 'Top'),
        (BASE, 'Base'),
        (BOTTOM, 'Bottom'),
    )
    order = models.ForeignKey(WorkingOrder, related_name='mouldings')
    num = models.PositiveIntegerField()
    type = models.PositiveSmallIntegerField(choices=TYPE_CHOICES)
    name = models.CharField(max_length=255)
    
    class Meta:
        ordering = ['type', 'num']
    
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
                
            


class AttachPreview(models.Model):
    "Stores PDF pages converted to images"
    attachment = models.ForeignKey(Attachment)
    page = models.PositiveIntegerField()
    file = models.ImageField(upload_to='data/wizard/attachments/%Y/%m/preview')
    
    class Meta:
        ordering = ['page']
    

class Appliance(models.Model):
    TYPES = ['Refrigerator', 'Microwave','Double sink','Cooktop','Oven']
    
    order = models.ForeignKey(WorkingOrder)
    type = models.CharField(max_length=100, choices=[(i,i) for i in TYPES])
    description = models.CharField(max_length=255, null=True, blank=True)
    width = DimensionField(null=True, blank=True)
    height = DimensionField(null=True, blank=True)
    depth = DimensionField(null=True, blank=True)
    
    def __unicode__(self):
        return self.type
