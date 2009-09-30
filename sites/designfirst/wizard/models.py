from django.db import models

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
    cabinet_door_style = models.CharField(max_length=150, blank=True, null=True, 
        verbose_name='Door Style')
    cabinet_wood = models.CharField(max_length=150, blank=True, null=True, 
        verbose_name='Wood')
    cabinet_finish = models.CharField(max_length=150, blank=True, null=True, 
        verbose_name='Other Finish')
    cabinet_finish_options =  models.CharField(max_length=150, blank=True, null=True, 
        verbose_name='Special Options')
    cabinetry_notes =  models.TextField('Notes', null=True, blank=True)
    
    
    #Hardware page
    HANDLE_PULL, HANDLE_KNOB = range(1,3)
    HANDLE_TYPES = (
            (HANDLE_PULL, 'Pull'),
            (HANDLE_KNOB, 'Knob'))
    
    door_handle_type = models.PositiveSmallIntegerField(choices=HANDLE_TYPES, null=True, blank=True)
    door_handle_model = models.CharField(max_length=255, null=True, blank=True)
    
    drawer_handle_type = models.PositiveSmallIntegerField(choices=HANDLE_TYPES, null=True, blank=True)
    drawer_handle_model = models.CharField(max_length=255, null=True, blank=True)
    
    #Moulding page
    celiling_height = models.CharField(max_length=255, null=True, blank=True)
    crown_moulding_type = models.CharField(max_length=255, null=True, blank=True)
    skirt_moulding_type = models.CharField(max_length=255, null=True, blank=True)
    soft_width = models.IntegerField('Width', null=True, blank=True)
    soft_height = models.IntegerField('Height', null=True, blank=True)
    soft_depth = models.IntegerField('Depth', null=True, blank=True)
    
    
    #Dimension page
    S_NORMAL, S_STACKED, S_STAGGERED = range(1,4)
    STYLE_CHOICES = (
            (S_NORMAL, 'Normal'),
            (S_STACKED, 'Stacked'),
            (S_STAGGERED, 'Staggered'))
    STANDARD_SIZES = [16, 32, 36]
    dimension_style = models.PositiveSmallIntegerField(choices=STYLE_CHOICES, null=True, blank=True)
    standard_sizes = models.BooleanField('Standard sizes')   
    wall_cabinet_height = models.PositiveIntegerField(null=True, blank=True)
    vanity_cabinet_height = models.PositiveIntegerField(null=True, blank=True)
    depth = models.PositiveIntegerField(null=True, blank=True)
    
    #Corder cabinet page
    BC_LEFT_OPENING, BC_OTHER_OPT = range(1,3)
    BUILD_CORNER_CHOICES = (
            (BC_LEFT_OPENING, 'Left Opening'),
            (BC_OTHER_OPT, 'Some other option'))
    build_corner_base = models.BooleanField()
    corder_base = models.PositiveSmallIntegerField(choices=BUILD_CORNER_CHOICES, null=True, blank=True)
    build_corner_wall = models.BooleanField()
    corner_wall = models.PositiveSmallIntegerField(choices=BUILD_CORNER_CHOICES, null=True, blank=True)
    
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
    
    
    
            