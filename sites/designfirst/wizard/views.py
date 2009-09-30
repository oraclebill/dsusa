from django.utils import simplejson
from django.http import HttpResponse
from base import WizardBase
from validation.models import Manufacturer, DoorStyle, WoodOption, FinishOption
from forms import *





class Wizard(WizardBase):
    
    steps = ['manufacturer', 'hardware', 'moulding', 'dimensions', 
             'corner_cabinet']
    
    def step_manufacturer(self, request):
        manufacturers = list(Manufacturer.objects.all())
        manufacturers_json = simplejson.dumps([m.json_dict() for m in manufacturers])
        return self.handle_form(request, ManufacturerFrom
                                , {'manufacturers': manufacturers,
                                   'manufacturers_json':manufacturers_json})
    
    
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



def _manufacturer_related(request, model):
    "Retrun JSON response of objects that matches manufacturer"
    manufacturer = request.GET.get('manufacturer', '')
    items = model.objects.filter(manufacturer__name=manufacturer)
    items = [i.name for i in items]
    return HttpResponse('\n'.join(['%s|%s' % (i,i) for i in items]))

def ajax_door_style(request):
    return _manufacturer_related(request, DoorStyle)

def ajax_wood(request):
    return _manufacturer_related(request, WoodOption)

def ajax_finish(request):
    return _manufacturer_related(request, FinishOption)
