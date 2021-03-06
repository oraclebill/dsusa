# standard library imports
from datetime import datetime
import string
import random
import decimal

# third party library imports
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, \
    HttpResponseForbidden, HttpResponseNotAllowed, HttpResponseServerError
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.template.loader import render_to_string
from django.utils import simplejson
from django.contrib.auth.decorators import login_required


# foreign app imports
from accounting.models import register_design_order
from catalog.manufacturers import CabinetLine, Catalog
from product.cart import new_cart
from product.models import Product
from product.views import paypal_checkout
from utils.views import render_to
from accounting.models import register_design_order
import summary 

# local app imports
from wizard import WizardBase
from models import BaseOrder, WorkingOrder, Attachment, Appliance, Moulding
from forms import ApplianceForm, AttachmentForm, CornerCabinetForm, DimensionsForm
from forms import HardwareForm, InteriorsForm, ManufacturerForm, MiscellaneousForm
from forms import SoffitsForm, SubmitForm, MouldingForm, NewDesignOrderForm


LETTERS_AND_DIGITS = string.letters + string.digits
RUSH_PROD_ID = 20

ORDER_PREFIX = 'DDS-010'

@login_required
@render_to('orders/create_order.html')
def create_order(request, *args):
    """
    Create a new order.
    """
    
    # prevent staff from creating orders until UI support available
    if not request.account:
        return HttpResponseNotAllowed("Invalid Action - Not Allowed")
    
    tracking_code = "".join([random.choice(LETTERS_AND_DIGITS) for x in xrange(15)])
             
    if request.method == 'POST':
        form = NewDesignOrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = WorkingOrder.objects.create_order(request.user, 
                                                      form.cleaned_data['project_name'], 
                                                      form.cleaned_data['project_type'], 
                                                      form.cleaned_data['tracking_code'])
            order.save()                     
            floorplanfile = request.FILES.get('floorplan', None)   
            if floorplanfile:
                att = order.attachments.create(type=Attachment.Const.FLOORPLAN, file=floorplanfile, source=Attachment.Const.UPLOADED)
                att.save()
                att.split_pages()
            return HttpResponseRedirect(reverse("order-wizard", args=[order.id]))
    else:
        form = NewDesignOrderForm(initial=dict(tracking_code=tracking_code))
    
    return dict(account=request.account, form=form, tracking_code=tracking_code)

@login_required
@render_to('orders/order_review.html')
def review_order(request, orderid):
    
    if request.user.is_staff:
        order = WorkingOrder.objects.get(pk=orderid)
    else:
        order = request.user.workingorder_set.get(pk=orderid)
        
#    user = request.user
    if request.method == 'POST':
        form = SubmitForm(request.POST, instance=order)
    else:
        form = SubmitForm(instance=order)
        
    order_info = summary.order_summary(order, summary.SUBMIT_SUMMARY)
    result_summary = summary.order_summary(order, summary.STEPS_SUMMARY)
    return {'order': order, 'order_info': order_info, 'data': result_summary, 'form':form, 'wizard': wizard}

    
@login_required
def print_order(request, id, template='orders/print_order.html', include_summary=True, extra_context={}):
    order = get_object_or_404(WorkingOrder, id=id)
    context = {'order': order }
            
    if include_summary:
        s = summary.order_summary(order, summary.STEPS_SUMMARY)
        #making two columns display
        l = len(s)/2
        s = s[:l], s[l:]
        context['summary'] = s
        
    if extra_context:
        context.update(extra_context)
        
    return render_to_response(template, context, context_instance=RequestContext(request))

@login_required
@transaction.commit_on_success
@render_to('orders/simple_submit.html')
def submit_order(request, orderid):
    """
    Change the order status from CLIENT_EDITING to CLIENT_SUBMITTED, and notify waiters.
    
    TODO - error handling, logging, 
    """
    if request.user.is_staff:
        order = WorkingOrder.objects.get(pk=orderid)
    else:
        order = request.user.workingorder_set.get(id=orderid) 

    if order.status != BaseOrder.Const.DEALER_EDIT:
        return HttpResponseServerError()
    
    # always submit orders in the context of proper account
    account = order.owner.get_profile().account
    
    if request.method == 'GET': 
        form = SubmitForm(instance=order)
    else:
        form = SubmitForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save(commit=False)
            cost = order.cost or decimal.Decimal()      
            if cost > account.credit_balance:
                ## users account doesn't have enough juice.. send then to the ecom engine 
                ## to pay, then get them back here ...
                order = form.save()
                products = [form.cleaned_data['design_product']]
                option = form.cleaned_data.get('processing_option', None)
                if option:
                    products.append(option)                    
                new_cart(request, products)
                request.method = 'GET'                
                return paypal_checkout(request, success_url=reverse('submit-order', args=[orderid]))
            else:           
                register_design_order(order.owner, order.owner.get_profile().account, order, cost)
                order = form.save(commit=False)
                order.status = BaseOrder.Const.SUBMITTED
                order.submitted = datetime.now()
                order.save()
            # return HttpResponseRedirect('completed_order_summary', args=[orderid]) # TODO
            return HttpResponseRedirect(reverse('submit-order-completed', args=[order.id]))              
    return dict(order=order, form=form)
    
    
@login_required
def delete_order(request, orderid, return_to):
    # verify permissions
    order = WorkingOrder.objects.get(pk=orderid)
    user = request.user
    if order.owner != request.user:
        if not user.has_perm('workingorder.delete'):
            return HttpResponseForbidden('You do not have permission to delete this order.')
    context = dict(order=order)
    if request.POST.get('post'):
        order.delete()
        return HttpResponseRedirect(return_to)
        
    return render_to_response('orders/confirm_delete.html', context, context_instance=RequestContext(request))
        
    
    
def complete_order(request, orderid):
    pass


@login_required
@render_to('orders/confirm_submission.html')
def post_submission_details(request, orderid):
    return dict(order=get_object_or_404(WorkingOrder, id=orderid))    
    
class Wizard(WizardBase):
    
    steps = ['manufacturer', 'hardware', 'moulding', 'soffits', 'configuration', 
             'corner_cabinet', 'interiors', 'miscellaneous', 
             'appliances', 'diagrams', 'review']
    def step_manufacturer(self, request):
        catalog = Catalog()
        manufacturers = catalog.manufacturers()

        return self.handle_form(request, ManufacturerForm, {
            'manufacturers_json': simplejson.dumps(manufacturers),
            'cabinet_lines': catalog.values(),
            'manufacturers': manufacturers,
            'default_selects': simplejson.dumps({
                'id_cabinet_material': ManufacturerForm.DOOR_MATERIALS,
                'id_finish_type': ManufacturerForm.FINISHES,
             })
        })

    def step_hardware(self, request):
        return self.handle_form(request, HardwareForm)

    def step_moulding(self, request):
        page_note = self.get_page_note()        
        if  request.method == 'POST' and self.order.status != WorkingOrder.Const.DEALER_EDIT:
            if 'add_moulding' in request.POST or 'delete' in request.POST or 'order' in request.POST:
                return HttpResponseForbidden('Order is not editable.')
            else: 
                return self.dispatch_next_step()             
        elif request.method == 'POST': # Ajax submit of new moulding
            new_page_note = request.POST.get('section_notes', page_note)
            if new_page_note != page_note:
                self.set_page_note(request.user.id, new_page_note)
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
                self.order.finish_step(self.step)
                return self.dispatch_next_step()
            items = Moulding.groups(self.order)
            return HttpResponse(render_to_string(
                        'wizard/moulding_items.html', {'items':items}))
            
        form = MouldingForm()
        return {'form': form, 'items': Moulding.groups(self.order),  'section_notes': page_note}
    
    def step_soffits(self, request):
        return self.handle_form(request, SoffitsForm)
    
    
    def step_configuration(self, request):
        standart_sizes = simplejson.dumps(WorkingOrder.STANDARD_SIZES)
        #when the manufacturer is one of the valid manufacturers, 
        #default 'Standard Sizes' should be 'checked' or 'True', 
        #otherwise false. :
        if self.order.wall_cabinet_height is None\
                and self.order.wall_cabinet_height is None\
                and self.order.wall_cabinet_height is None:
            self.order.standard_sizes = is_existing_manufacturer(self.order)
        context = {
            'standard_sizes': standart_sizes,
        }
        return self.handle_form(request, DimensionsForm, context)
    step_configuration.title = summary.DIMENSION_SECTION[0]
    
    
    def step_corner_cabinet(self, request):
        return self.handle_form(request, CornerCabinetForm)
    
    def step_interiors(self, request):
        return self.handle_form(request, InteriorsForm)
    
    def step_miscellaneous(self, request):
        return self.handle_form(request, MiscellaneousForm)
    
    def step_appliances(self, request):
        # short circuit all mutators if not in edit mode...
        if self.order.status != WorkingOrder.Const.DEALER_EDIT:
            if request.method == 'POST' and 'add_appliance' in request.POST:
                return HttpResponseForbidden('Order is locked.')
            elif request.method == 'GET' and 'delete' in request.GET:
                return HttpResponseForbidden('Order is locked.')
            elif request.method == 'POST':
                return self.dispatch_next_step()                                
             
        page_note = self.get_page_note()
        if request.method == 'POST':
            new_page_note = request.POST.get('section_notes', page_note)
            if new_page_note != page_note:
                self.set_page_note(request.user.id, new_page_note)
            if 'add_appliance' in request.POST:
                form = ApplianceForm(request.POST, request.FILES)
                if form.is_valid():
                    obj = form.save(commit=False)
                    obj.order = self.order
                    obj.save()
            else:
                self.order.finish_step(self.step)
                return self.dispatch_next_step()                
        else:
            if 'delete' in request.GET:
                appliance = get_object_or_404(Appliance, order=self.order, 
                                           id=int(request.GET['delete']))
                appliance.delete()
                return HttpResponseRedirect('./')
        form = ApplianceForm()
        appliances = Appliance.objects.filter(order=self.order)
        return {'form': form, 'appliances': appliances, 'section_notes': page_note }
    
    def step_diagrams(self, request):
        context = {}
        # short circuit all mutators if not in edit mode...
        if self.order.status != WorkingOrder.Const.DEALER_EDIT:
            if request.method == 'POST':
                return self.dispatch_next_step()
            if 'delete' in request.GET:
                return HttpResponseRedirect('./')
            
        if request.method == 'POST':
            if 'upload_file' not in request.POST:
                self.order.finish_step(self.step)
                return self.dispatch_next_step()
            form = AttachmentForm(request.POST, request.FILES)
            if form.is_valid():
                obj = form.save(commit=False)
                obj.order = self.order
                obj.save()
                if obj.file.path.lower().endswith('pdf'):
                    obj.split_pages()
#                context['confirm_attach'] = obj.id                
            return HttpResponseRedirect('./')

        # GET processing
        form = AttachmentForm()
        if 'delete' in request.GET:
            attach = get_object_or_404(Attachment, order=self.order, 
                                       id=int(request.GET['delete']))
            attach.delete()
            return HttpResponseRedirect('./')
        attachments = Attachment.objects.filter(order=self.order)
        context.update({'form': form, 'order': self.order, 'attachments': attachments})
        return context
    
    def step_review(self, request):
        if request.method == 'POST':
            #TODO: check if the order is complete!
            return self.dispatch_next_step()
        return dict(form=SubmitForm())
        
    def complete(self, request):
        order = self.order
        if order.is_complete():
            return HttpResponseRedirect(reverse('submit-order', args=[order.id]))
        else:
            return dict()

    def get_summary(self):
        return summary.order_summary(self.order, summary.STEPS_SUMMARY)

@login_required
def wizard(request, id, step=None, complete=False):
    return Wizard()(request, id, step, complete)


def is_existing_manufacturer(order):
#     return order.manufacturer in get_manufacturers()
    return False



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
    lines = Catalog().cabinet_line(mfg).product_lines
    return HttpResponse(simplejson.dumps(lines))

def ajax_door_style(request):
    mfg = request.GET.get('m', None)
    if not mfg:
        return HttpResponse()    
    styles = Catalog().cabinet_line(mfg).get_door_styles(species=request.GET.get('dm', None))
#    return HttpResponse(['%s|%s' % (s,s) for s in styles]) # if q in style])
    return HttpResponse(simplejson.dumps(styles)) # if q in style])
 
def ajax_wood(request):
    mfg = request.GET.get('m', None)
    if not mfg:
        return HttpResponse()
    species = Catalog().cabinet_line(mfg).get_door_materials(style=request.GET.get('ds', None))
    #return HttpResponse('\n'.join(['%s|%s' % (a,a) for a in species])) # if q in style])
    return HttpResponse(simplejson.dumps(species)) # if q in style])

def ajax_finish_color(request):
    mfg = request.GET.get('m', None)
    if not mfg:
        return HttpResponse()
    finish = Catalog().cabinet_line(mfg).get_primary_finishes(species=request.GET.get('dm', None), 
                                                               finish_type=request.GET.get('ft', None), 
                                                               style=request.GET.get('ds', None))
    return HttpResponse(simplejson.dumps(finish)) # if q in style])


def ajax_manufacturer(request):
    catalog = Catalog()

    def material_data(material, cabinet_line):
        finish_types = cabinet_line.get_primary_finish_types(material)
        finish_types_data = {}
        for finish_type in finish_types:
            colors = cabinet_line.get_primary_finishes(species=material)
            finish_types_data[finish_type] = {'colors': colors}

        return {
            'name': material,
            'door_style': cabinet_line.get_door_styles(material),
            'finish_type': finish_types_data,
            'finish_options': cabinet_line.get_finish_option_types(material),
            'finish_color': cabinet_line.get_primary_finishes(species=material),
        }

    def manufacturer_data(cabinet_line):
        return {
            'name': manufacturer,
            'product_line': cabinet_line.product_lines,
            'material': dict((
                (material, material_data(material, cabinet_line))
                for material in cabinet_line.get_door_materials()
             )),
            'materials_list': cabinet_line.get_door_materials(),
        }

    manufacturer = request.GET.get('manufacturer', None)
    try:
        cabinet_line = catalog.cabinet_line(manufacturer)
    except KeyError:
        res = {'error': 'DoesNotExist'}
    else:
        res = manufacturer_data(cabinet_line)

    return HttpResponse(simplejson.dumps(res), mimetype="application/javascript")


@render_to('orders/fragments/attachment_list.html')
def attachment_list(request, orderid):
    order = get_object_or_404(WorkingOrder, id=orderid)
    # TODO: permissions
    attachments = order.attachments.all() 
    return {'attachments': attachments}
    
@render_to('orders/fragments/attachment_details.html')
def attachment_details(request, orderid, attachmentid):
    attachment = get_object_or_404(Attachment, id=attachmentid)
    if not attachment.order.id == orderid:
        return HttpResponseNotFound('%s for %d' % (attachmentid, orderid))
    return {'attachment': attachment}
    
def attachment_upload(request, orderid):
    #import pdb; pdb.set_trace()
    order = get_object_or_404(WorkingOrder, id=orderid)
    if request.method == 'POST' and request.FILES:
        upload = order.attachments.create()
        upload.timestamp = datetime.now()
        try:
            upload.type = int(request.POST['type'])
        except:
            pass  # default         
        if upload.type in ('jpg', 'png', 'gif', 'bmp'):
            upload.page_count = 1
        else: 
            upload.page_count = 0
        upload.file = request.FILES['Filedata']
        upload.save()
        return HttpResponse(True)
    return HttpResponseServerError("Fail")

    
