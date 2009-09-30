from django.utils import simplejson
from django.http import HttpResponse
from base import WizardBase
from validation.models import Manufacturer, DoorStyle, WoodOption, FinishOption
from forms import *


class Wizard(WizardBase):
    
    steps = ['manufacturer', 'hardware', 'moulding', 'dimensions', 
             'corner_cabinet', 'miscellaneous', 'attachments']
    
    def step_manufacturer(self, request):
        manufacturers = list(Manufacturer.objects.all())
        manufacturers_json = simplejson.dumps([m.json_dict() for m in manufacturers])
        return self.handle_form(request, ManufacturerFrom
                                , {'manufacturers': manufacturers,
                                   'manufacturers_json':manufacturers_json})
    
    
    def step_hardware(self, request):
        return self.handle_form(request, HardwareFrom)
    
    
    def step_moulding(self, request):
        return self.handle_form(request, MouldingFrom)
    
    
    def step_dimensions(self, request):
        standart_sizes = simplejson.dumps(WorkingOrder.STANDARD_SIZES)
        return self.handle_form(request, DimensionsForm, {'standard_sizes':standart_sizes})
    step_dimensions.title = 'Corner boxes'
    
    
    def step_corner_cabinet(self, request):
        return self.handle_form(request, CornerCabinetForm)
    
    def step_miscellaneous(self, request):
        return self.handle_form(request, MiscellaneousForm)
    
    def step_attachments(self, request):
        if request.method == 'POST':
            if 'save_next' in request.POST:
                return self.next_step()
            form = AttachmentForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.order = self.order
                obj.save()
        else:
            form = AttachmentForm()
        attachments = Attachment.objects.filter(order=self.order)
        return {'form': form, 'attachments': attachments}
    
    def complete(self, request):
        return HttpResponse("Wizard is complete")
    
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
            ('Moulding', [
                'celiling_height',
                'crown_moulding_type',
                'skirt_moulding_type',
                'soft_width',
                'soft_height',
                'soft_depth',
            ]),
            ('Dimensions', [
                'dimension_style',
                'standard_sizes',
                'wall_cabinet_height',
                'vanity_cabinet_height',
                'depth'
            ]),
            ('Corner cabinet', [
                'build_corner_base',
                'corder_base',
                'build_corner_wall',
                'corner_wall',
            ]),
            ('Miscellaneous', [
                'corables',
                'brackets',
                'valance',
                'leas_feet',
                'glass_doors',
                'range_hood',
                'posts',
            ]),
        ]
        return self._get_summary(summary_fields)
        



def wizard(request, id, step=None, complete=False):
    return Wizard()(request, id, step, complete)



def _manufacturer_related(request, model):
    "Retrun 'autocomplete' response of objects that matches manufacturer"
    manufacturer = request.GET.get('manufacturer', '')
    q = request.GET['q']
    items = model.objects.filter(manufacturer__name=manufacturer, name__icontains=q)
    items = [i.name for i in items]
    return HttpResponse('\n'.join(['%s|%s' % (i,i) for i in items]))

def ajax_door_style(request):
    return _manufacturer_related(request, DoorStyle)

def ajax_wood(request):
    return _manufacturer_related(request, WoodOption)

def ajax_finish(request):
    return _manufacturer_related(request, FinishOption)
