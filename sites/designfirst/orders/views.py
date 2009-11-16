
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect,\
    HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

from catalog.manufacturers import CabinetLine, Catalog
from utils.views import render_to

from base import WizardBase
from models import WorkingOrder, Attachment, Appliance, Moulding
from forms import ApplianceForm, AttachmentForm, CornerCabinetForm, DimensionsForm
from forms import HardwareForm, InteriorsForm, ManufacturerForm, MiscellaneousForm
from forms import SoffitsForm, SubmitForm, MouldingForm
#from forms import * 
import summary 



class Wizard(WizardBase):
    
    steps = ['manufacturer', 'hardware', 'moulding', 'soffits', 'dimensions', 
             'corner_cabinet', 'interiors', 'miscellaneous', 
             'appliances', 'diagrams', 'order_review']
    
    def step_manufacturer(self, request):
        manufacturers = {}
        manufacturers = Catalog().manufacturers()
        # manufacturers_json = simplejson.dumps([m.json_dict() for m in manufacturers])
        return self.handle_form(request, ManufacturerForm,
                                 {'manufacturers_json': simplejson.dumps(manufacturers),
                                   'manufacturers':manufacturers})
    
    
    def step_hardware(self, request):
        return self.handle_form(request, HardwareForm)
    
    
    def step_moulding(self, request):
        if request.method == 'POST': # Ajax submit of new moulding
            if 'add_moulding' in request.POST:
                form = MouldingForm(request.POST)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.order = self.order
                    obj.save()
            elif 'delete' in request.POST:
                obj = get_object_or_404(self.order.mouldings.all(), 
                                  pk=int(request.POST['delete']))
                obj.delete()
            elif 'order' in request.POST:
                sort_order = map(int, [i for i in request.POST['order'].split(',') if len(i) > 0])
                Moulding.reorder(self.order, int(request.POST['type']), sort_order)
            else:
                return self.dispatch_next_step()
            items = Moulding.groups(self.order)
            return HttpResponse(render_to_string(
                        'wizard/moulding_items.html', {'items':items}))
        form = MouldingForm()
        return {'form': form, 'items': Moulding.groups(self.order)}
    
    def step_soffits(self, request):
        return self.handle_form(request, SoffitsForm)
    
    
    def step_dimensions(self, request):
        standart_sizes = simplejson.dumps(WorkingOrder.STANDARD_SIZES)
        images = {
            WorkingOrder.S_NONE: None,
            WorkingOrder.S_STACKED: 'S_STACKED.png',
            WorkingOrder.S_STG_HWC: 'S_STG_HWC.png',
            WorkingOrder.S_STG_DHWC: 'S_STG_DHWC.png',
            WorkingOrder.S_STG_HBC: 'S_STG_HBC.png',
            WorkingOrder.S_STG_DBC: 'S_STG_DBC.png',
        }
        images_base = settings.MEDIA_URL + 'images/stacking_staggering/'
        #when the manufacturer is one of the valid manufacturers, 
        #default 'Standard Sizes' should be 'checked' or 'True', 
        #otherwise false. :
        if self.order.wall_cabinet_height is None\
                and self.order.wall_cabinet_height is None\
                and self.order.wall_cabinet_height is None:
            self.order.standard_sizes = is_existing_manufacturer(self.order)
        context = {
            'standard_sizes': standart_sizes,
            'stack_images': simplejson.dumps(images),
            'stack_images_base': images_base,
        }
        return self.handle_form(request, DimensionsForm, context)
    step_dimensions.title = summary.DIMENSION_SECTION[0]
    
    
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
                return HttpResponseRedirect(request.META['HTTP_REFERER'])
                return HttpResponseRedirect('./')
            form = AttachmentForm()
            form = ApplianceForm()
        appliances = Appliance.objects.filter(order=self.order)
        return {'form': form, 'appliances': appliances}
    
    def step_diagrams(self, request):
        context = {}
        if request.method == 'POST':
            if 'upload_file' not in request.POST:
                return self.dispatch_next_step()
            form = AttachmentForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.order = self.order
                obj.save()
                if obj.is_multipage:
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
    
    def step_order_review(self, request):
        return _order_review(request, self)
    
    def get_summary(self):
        return summary.order_summary(self.order, summary.STEPS_SUMMARY)


@login_required
def wizard(request, id, step=None, complete=False):
    return Wizard()(request, id, step, complete)

@render_to('wizard/order_review.html')
def _order_review(request, wizard):
    order = wizard.order
    if request.method == 'POST':
        form = SubmitForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            order.status = WorkingOrder.SUBMITTED
            order.save()
            return HttpResponseRedirect('/dealer/')
    else:
        form = SubmitForm(instance=order)
    result_summary = summary.order_summary(order, summary.SUBMIT_SUMMARY)
    exclude = ['owner', 'status', 'project_name', 'desired', 'cost', 'id']
    for title, excl in summary.SUBMIT_SUMMARY:
        exclude += excl
    OPT_FIELDS = [f.name for f in order._meta.fields if f.name not in exclude and f.editable]
    result_summary += summary.order_summary(order, [('Options', OPT_FIELDS)])
    return {'order': order, 'data': dict(result_summary), 'form':form, 'wizard': wizard}

@render_to('print_order.html')
def print_order(request, id):
    order = get_object_or_404(WorkingOrder, id=id)
    if order.owner.id != request.user.id:
        return HttpResponseForbidden("Not allowed to view this order")
    summary = summary.order_summary(order, summary.STEPS_SUMMARY)
    #making two columns display
    l = len(summary)/2
    summary = summary[:l], summary[l:]
    return {'order': order, 'summary': summary}

def is_existing_manufacturer(order):
    return order.manufacturer in get_manufacturers()

@render_to('wizard/attachment_details.html')
def ajax_attach_details(request, id):
    attachment = get_object_or_404(Attachment, id=id)
    return {'attachment': attachment}

def _make_kwargs(request, keys=['ds', 'dm', 'ft']):
    kwargs = {}
    keymap = {'ds': 'style', 'dm': 'species', 'ft': 'finish_type'}
    for key in keys:
        if key in request.GET: kwargs[keymap[key]] = request.GET[key]
    return kwargs

def ajax_product_line(request):
    mfg = request.GET.get('m', None)
    if not mfg:
        return HttpResponse()    
    lines = [mfg]
    return HttpResponse(simplejson.dumps(lines))

def ajax_door_style(request):
    mfg = request.GET.get('m', None)
    if not mfg:
        return HttpResponse()    
    styles = Catalog().cabinet_line(mfg).get_door_styles(species=request.GET.get('dm', None))
    return HttpResponse(['%s|%s' %s for s in styles]) # if q in style])
 
def ajax_wood(request):
    mfg = request.GET.get('m', None)
    if not mfg:
        return HttpResponse()
    species = Catalog().cabinet_line(mfg).get_door_materials(style=request.GET.get('ds', None))
    return HttpResponse('\n'.join(['%s|%s' % (a,a) for a in species])) # if q in style])
    return HttpResponse(simplejson.dumps(species)) # if q in style])

def ajax_finish_color(request):
    mfg = request.GET.get('m', None)
    if not mfg:
        return HttpResponse()
    finish = Catalog().cabinet_line(mfg).get_primary_finishes(species=request.GET.get('dm', None), 
                                                               finish_type=request.GET.get('ft', None), 
                                                               style=request.GET.get('ds', None))
    return HttpResponse(simplejson.dumps(finish)) # if q in style])
