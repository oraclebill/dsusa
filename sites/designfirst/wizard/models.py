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
    cabinet_stain = models.CharField(max_length=150, blank=True, null=True, 
        verbose_name='Stain')
    cabinet_finish = models.CharField(max_length=150, blank=True, null=True, 
        verbose_name='Other Finish')
    cabinet_finish_options =  models.CharField(max_length=150, blank=True, null=True, 
        verbose_name='Special Options')
    cabinetry_notes =  models.CharField(max_length=150, blank=True, null=True, 
        verbose_name='Notes')
    
    
    #Hardware page
    HANDLE_PULL, HANDLE_KNOB = range(1,3)
    HANDLE_TYPES = (
            (HANDLE_PULL, 'Pull'),
            (HANDLE_KNOB, 'Knob'))
    
    door_handle_type = models.PositiveSmallIntegerField(choices=HANDLE_TYPES, null=True, blank=True)
    door_handle_model = models.CharField(max_length=255, null=True, blank=True)
    
    drawer_handle_type = models.PositiveSmallIntegerField(choices=HANDLE_TYPES, null=True, blank=True)
    drawer_handle_model = models.CharField(max_length=255, null=True, blank=True)
    
    
    
    
    
    
    
    
    
    def __unicode__(self):
        return self.project_name
    
    
    
            