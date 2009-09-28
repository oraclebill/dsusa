from base import WizardBase
from forms import *





class Wizard(WizardBase):
    
    steps = ['manufacturer', 'hardware', 'moulding', 'dimensions', 
             'corner_cabinet']
    
    def step_manufacturer(self, request):
        return self.handle_form(request, ManufacturerFrom)
    
    
    def step_hardware(self, request):
        return self.handle_form(request, HardwareFrom)
    
    
    def step_moulding(self, request):
        return self.handle_form(request, MockForm)
    
    
    def step_dimensions(self, request):
        return self.handle_form(request, MockForm)
    step_dimensions.title = 'Corner boxes'
    
    
    def step_corner_cabinet(self, request):
        return self.handle_form(request, MockForm)
    
    def get_summary(self):
        summary_fields = [
            ('Manufacturer', [
                'cabinet_manufacturer',
                'cabinet_door_style',
                'cabinet_wood',
                'cabinet_stain',
                'cabinet_finish',
            ]),
            ('Hardware', [
                'door_handle_type',
                'door_handle_model',
                'drawer_handle_type',
                'drawer_handle_model',
            ]),
            ('Manufacturer', [
                
            ]),
        ]
        return self._get_summary(summary_fields)
        



def wizard(request, id, step=None):
    return Wizard()(request, id, step)
