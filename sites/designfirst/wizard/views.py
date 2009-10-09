from django.utils import simplejson
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from base import WizardBase
from validation.models import Manufacturer, DoorStyle, WoodOption, FinishOption
from utils.views import render_to
from models import Attachment, Appliance
from forms import *
from summary import order_summary, STEPS_SUMMARY, SUBMIT_SUMMARY




class Wizard(WizardBase):
    
    steps = ['manufacturer', 'hardware', 'moulding', 'soffits', 'dimensions', 
             'corner_cabinet', 'interiors', 'miscellaneous', 
             'appliances', 'attachments']
    
    def step_manufacturer(self, request):
        manufacturers = list(Manufacturer.objects.all())
        manufacturers_json = simplejson.dumps([m.json_dict() for m in manufacturers])
        return self.handle_form(request, ManufacturerForm
                                , {'manufacturers': manufacturers,
                                   'manufacturers_json':manufacturers_json})
    
    
    def step_hardware(self, request):
        return self.handle_form(request, HardwareForm)
    
    
    def step_moulding(self, request):
        return self.handle_form(request, MouldingForm)
    
    def step_soffits(self, request):
        return self.handle_form(request, SoffitsForm)
    
    
    def step_dimensions(self, request):
        standart_sizes = simplejson.dumps(WorkingOrder.STANDARD_SIZES)
        #when the manufacturer is one of the valid manufacturers, 
        #default 'Standard Sizes' should be 'checked' or 'True', 
        #otherwise false. :
        if self.order.wall_cabinet_height is None\
                and self.order.wall_cabinet_height is None\
                and self.order.wall_cabinet_height is None:
            self.order.standard_sizes = is_existing_manufacturer(self.order)
        return self.handle_form(request, DimensionsForm, {'standard_sizes':standart_sizes})
    step_dimensions.title = 'Corner boxes'
    
    
    def step_corner_cabinet(self, request):
        return self.handle_form(request, CornerCabinetForm)
    
    def step_interiors(self, request):
        return self.handle_form(request, InteriorsForm)
    
    def step_miscellaneous(self, request):
        return self.handle_form(request, MiscellaneousForm)
    
    def step_appliances(self, request):
        if request.method == 'POST':
            if 'add_appliance' not in request.POST:
                return self.dispatch_next_step()
            form = ApplianceForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.order = self.order
                obj.save()
                form = ApplianceForm()
        else:
            if 'delete' in request.GET:
                appliance = get_object_or_404(Appliance, order=self.order, 
                                           id=int(request.GET['delete']))
                appliance.delete()
                return HttpResponseRedirect('./')
            form = AttachmentForm()
            form = ApplianceForm()
        appliances = Appliance.objects.filter(order=self.order)
        return {'form': form, 'appliances': appliances}
    
    def step_attachments(self, request):
        context = {}
        if request.method == 'POST':
            if 'upload_file' not in request.POST:
                return self.dispatch_next_step()
            form = AttachmentForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.order = self.order
                obj.save()
                if obj.is_pdf():
                    obj.generate_pdf_previews()
                context['confirm_attach'] = obj.id
                
        else:
            if 'delete' in request.GET:
                attach = get_object_or_404(Attachment, order=self.order, 
                                           id=int(request.GET['delete']))
                attach.delete()
                return HttpResponseRedirect('./')
            form = AttachmentForm()
        attachments = Attachment.objects.filter(order=self.order)
        context.update({'form': form, 'attachments': attachments})
        return context
    
    def complete(self, request):
        return _complete_wizard(request, self.order)
    
    def get_summary(self):
        return order_summary(self.order, STEPS_SUMMARY)
        



def wizard(request, id, step=None, complete=False):
    return Wizard()(request, id, step, complete)

@render_to('submit_order.html')
def _complete_wizard(request, order):
    if request.method == 'POST':
        order.status = WorkingOrder.SUBMITTED
        order.save()
        return HttpResponseRedirect('/dealer/')
    summary = order_summary(order, SUBMIT_SUMMARY)
    exclude = ['owner', 'status', 'project_name', 'desired', 'cost', 'id']
    for title, excl in SUBMIT_SUMMARY:
        exclude += excl
    OPT_FIELDS = [f.name for f in order._meta.fields if f.name not in exclude]
    summary += order_summary(order, [('Options', OPT_FIELDS)])
    return {'order': order, 'data': dict(summary)}

def is_existing_manufacturer(order):
    #TODO: move to Manufacturer model
    try:
        Manufacturer.objects.get(name=order.cabinet_manufacturer)
        return True
    except Manufacturer.DoesNotExist:
        return False


def _manufacturer_related(request, model):
    "Retrun 'autocomplete' response of objects that matches manufacturer"
    manufacturer = request.GET.get('manufacturer', '')
    q = request.GET['q']
    items = model.objects.filter(manufacturer__name=manufacturer, name__icontains=q)
    items = [i.name for i in items]
    return HttpResponse('\n'.join(['%s|%s' % (i,i) for i in items]))


@render_to('wizard/attachment_details.html')
def ajax_attach_details(request, id):
    attachment = get_object_or_404(Attachment, id=id)
    return {'attachment': attachment}

def ajax_door_style(request):
    return _manufacturer_related(request, DoorStyle)

def ajax_wood(request):
    return _manufacturer_related(request, WoodOption)

def ajax_finish(request):
    return _manufacturer_related(request, FinishOption)
