# standard library imports
from datetime import datetime
import string
import random
import decimal

# third party library imports
from django.core.urlresolvers import reverse
from django.conf import settings
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect,\
    HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.utils import simplejson
from django.contrib.auth.decorators import login_required

# foreign app imports
from accounting.models import register_design_order
from catalog.manufacturers import CabinetLine, Catalog
from product.cart import new_cart
from product.models import Product
from product.views import review_and_process_payment_info
from utils.views import render_to
from accounting.models import register_design_order
from customer.auth import active_dealer_only
import summary 

# local app imports
from base import WizardBase
from models import OrderBase, WorkingOrder, Attachment, Appliance, Moulding
from forms import ApplianceForm, AttachmentForm, CornerCabinetForm, DimensionsForm
from forms import HardwareForm, InteriorsForm, ManufacturerForm, MiscellaneousForm
from forms import SoffitsForm, SubmitForm, MouldingForm, NewDesignOrderForm


LETTERS_AND_DIGITS = string.letters + string.digits
RUSH_PROD_ID = 20

@login_required
@render_to('orders/create_order.html')
def create_order(request, *args):
    """
    Create a new order.
    """
    account = request.user.get_profile().account  
    tracking_code = "".join([random.choice(LETTERS_AND_DIGITS) for x in xrange(15)])
             
    if request.method == 'POST':
        form = NewDesignOrderForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.save(commit=False)
            order.client_account = account #TODO: there is actually no client_account in working order
            order.owner = request.user
            order.save()                     
            floorplanfile = request.FILES.get('floorplan', None)   
            if floorplanfile:
                att = order.attachments.create(type=Attachment.FLOORPLAN, file=floorplanfile, source=Attachment.UPLOADED)
                att.save()
                att.split_pages()
            return HttpResponseRedirect(reverse("order-wizard", args=[order.id]))
    else:
        form = NewDesignOrderForm(initial=dict(tracking_code=tracking_code))
    
    return dict(account=account, form=form, tracking_code=tracking_code)

@login_required
@render_to('orders/order_review.html')
def review_order(request, orderid):
    account = request.user.get_profile().account  
    order = request.user.workingorder_set.get(pk=orderid)
#    user = request.user
    if request.method == 'POST':
        form = SubmitForm(request.POST, instance=order)
#        if form.is_valid():
#            register_design_order(user, user.get_profile().account,
#                                  order, order.cost)
#            order = form.save(commit=False)
#            order.status = WorkingOrder.SUBMITTED
#            order.save()
#            return HttpResponseRedirect('/dealer/')
    else:
        form = SubmitForm(instance=order)
        
    result_summary = summary.order_summary(order, summary.SUBMIT_SUMMARY)
    exclude = ['owner', 'status', 'project_name', 'desired', 'cost', 'id']
    for title, excl in summary.SUBMIT_SUMMARY:
        exclude += excl
    OPT_FIELDS = [f.name for f in order._meta.fields if f.name not in exclude and f.editable]
    result_summary += summary.order_summary(order, [('Options', OPT_FIELDS)])
    return {'order': order, 'data': dict(result_summary), 'form':form, 'wizard': wizard}

@login_required
@render_to('orders/print_order.html')
def print_order(request, id):
    order = get_object_or_404(WorkingOrder, id=id)
    if order.owner.id != request.user.id:
        return HttpResponseForbidden("Not allowed to view this order")
    s = summary.order_summary(order, summary.STEPS_SUMMARY)
    #making two columns display
    l = len(s)/2
    s = s[:l], s[l:]
    return {'order': order, 'summary': s}

@login_required
@transaction.commit_on_success
@render_to('orders/simple_submit.html')
def submit_order(request, orderid):
    """
    Change the order status from CLIENT_EDITING to CLIENT_SUBMITTED, and notify waiters.
    
    TODO - error handling, logging, 
    """
    user = request.user
    if user is None or not user.is_authenticated():
        return HttpResponseRedirect('/')
 
    profile = user.get_profile()
    account = profile.account
    order = user.workingorder_set.get(id=orderid) 
    
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
                order.save()
                products = [form.cleaned_data['design_product']]
                option = form.cleaned_data.get('processing_option', None)
                if option:
                    products.append(option)                    
                new_cart(request, products)
                request.method = 'GET'                
                return review_and_process_payment_info(request, success_url=reverse('submit-order', args=[orderid]))
            else:           
                register_design_order(order.owner, order.owner.get_profile().account, order, cost)
                order.status = OrderBase.Const.SUBMITTED
                order.save()
            # return HttpResponseRedirect('completed_order_summary', args=[orderid]) # TODO
            return HttpResponseRedirect(reverse('submit-order-completed', args=[order.id]))              
    return dict(order=order, form=form)
    
@login_required
@render_to('orders/confirm_submission.html')
def post_submission_details(request, orderid):
    return dict(order=get_object_or_404(WorkingOrder, id=orderid))    
    
class Wizard(WizardBase):
    
    steps = ['manufacturer', 'hardware', 'moulding', 'soffits', 'dimensions', 
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
                if obj.file.path.lower().endswith('pdf'):
                    obj.split_pages()
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
@active_dealer_only
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
