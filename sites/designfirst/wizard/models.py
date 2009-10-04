from utils.fields import DimensionField
import os
from django.core.files.base import File as DjangoFile
from django.db import models
from utils.pdf import pdf2ppm

class WorkingOrder(models.Model):
    """
    This is a temporary object used for storing data 
    when  user goes step to step in wizard
    """
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
    
    #Moulding page
    celiling_height = models.CharField(max_length=255, null=True, blank=True)
    crown_moulding_type = models.CharField(max_length=255, null=True, blank=True)
    skirt_moulding_type = models.CharField(max_length=255, null=True, blank=True)
    soffit_width = DimensionField('Width', null=True, blank=True)
    soffit_height = DimensionField('Height', null=True, blank=True)
    soffit_depth = DimensionField('Depth', null=True, blank=True)
    
    
    #Dimension page
    S_NORMAL, S_STACKED, S_STAGGERED = range(1,4)
    STYLE_CHOICES = (
            (S_NORMAL, 'Normal'),
            (S_STACKED, 'Stacked'),
            (S_STAGGERED, 'Staggered'))
    STANDARD_SIZES = [16, 32, 36]
    dimension_style = models.PositiveSmallIntegerField(choices=STYLE_CHOICES, default=S_NORMAL)
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
        pdf2ppm(self.file.path, [(300, 600)], self._pdf_callback)
    
    def _pdf_callback(self, filename, page, size):
        preview = AttachPreview(page=page, attachment=self)
        file = DjangoFile(open(filename, 'rb'))
        preview.file.save(file.name, file)
        preview.save()

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
