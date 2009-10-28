##
## python imports
import logging as log
from datetime import datetime, timedelta
from decimal import Decimal

##
## library imports 

##
## django imports
from django.utils import simplejson
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from django.db import transaction


from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

##
## imports from other apps
from product.models import Product
from wizard.models import WorkingOrder, Appliance, Moulding, Attachment
from wizard import forms as wf
##
## local imports 
from constants import ACCOUNT_ID, ORDER_ID
from models import DealerOrganization, Transaction,UserProfile  
from forms import DesignOrderAcceptanceForm, NewDesignOrderForm, DealerProfileForm




##
## UTILITY FUNCTIONS
##

def get_current_order(request, orderid):
    """
    Get an order object by id, validating that the current user has access.
    
    TODO
    """
    
    user = request.user
    if user.is_authenticated():
        profile = user.get_profile()
        account = profile.account
        # order = account.created_orders.get(id=orderid)
        order = user.workingorder_set.get(id=orderid)
    else:
        raise PermissionDenied("You're not allowed here - anonymous users go home!")
    
    return order
    
# todo: create - /static/[inactive_user|login_failure|page_not_found]

##
## VIEW FUNCTIONS
##

def home(request):
    """
    Render the home page.
    
    TODO should be static?
    """
    
    return render_to_response( 'home/home.html',context_instance=RequestContext(request) )


def do_login(request):
    """
    Log user in and direct them to the proper area.
    
    TODO allow for chaining from unauthorized accesses.
    """
    
    username = request.POST['username']
    password = request.POST['password']
    login_message = None
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            try:
                profile = user.get_profile()
            except UserProfile.DoesNotExist:
                return HttpResponseRedirect(reverse('dealer-complete-profile') )                
                
            usertype = profile.usertype            
            return HttpResponseRedirect( '/%s/' % usertype )
        else:
            login_message="User is locked. Please contact support"
    else:
        login_message="Login failed."

    return render_to_response('home/home.html', 
        dict(login_message=login_message),
        context_instance=RequestContext(request))

def do_logout(request):
    """
    Log user out and direct them to the home page.
    
    TODO
    """
    
    try:
        request.session.flush()
    except:
        pass
    return HttpResponseRedirect(reverse('home.views.home'))

## FIXME: for now all users without profiles are assumed dealers.
def create_profile(request):
    user = request.user;
    
    if request.method == 'GET':
        form = DealerProfileForm(instance=user)
    else:
        form = DealerProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            ## FIXME: for now all users without profiles are assumed dealers.
            return HttpResponseRedirect('/dealer/')
            
    return render_to_response( 'profiles/create_profile.html', 
                locals(), 
                context_instance=RequestContext(request))
                
    
def dealer_dashboard(request):
    """
    Display summary information for areas of dealer interest, provide primary navigation to work areas.
    
    TODO - document
    """
    
    user = request.user
    if user is None or not user.is_authenticated():
        return HttpResponseRedirect('/')
    
    account = request.user.get_profile().account.dealerorganization
    
    # orders = account.created_orders.all()
    orders = user.workingorder_set.all()
    transactions = account.transaction_set.all()
    
    working_orders = orders.filter( status__exact = WorkingOrder.DEALER_EDIT )
    submitted_orders = orders.filter( status__in = [ WorkingOrder.SUBMITTED, WorkingOrder.ASSIGNED ] )
       ## TODO: fixme!
    archived_orders = orders.exclude( status__in = [ WorkingOrder.DEALER_EDIT, WorkingOrder.SUBMITTED, WorkingOrder.ASSIGNED ] ) 
        
    return render_to_response( 'home/dealer_dashboard.html', locals(),                                
                                context_instance=RequestContext(request) ) 
 

def create_order(request, *args):
    """
    Create a new order.
    """
    account = request.user.get_profile().account.dealerorganization              
    if request.method == 'POST':
        form = NewDesignOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client_account = account#TODO: there is actually no client_account in working order
            order.owner = request.user
            order.save()
                        
            return HttpResponseRedirect(reverse("order-wizard", args=[order.id]))
    else:
        desired = (datetime.now() + timedelta(days=2))
        form = NewDesignOrderForm(initial={'desired': desired, 'cost':None})
    
    #Prices is used to get price from product when user switches product in from
    prices = dict([(p.id, float(p.customer_price(account))) 
                   for p in Product.objects.all()])
    prices = simplejson.dumps(prices)
    return render_to_response('home/create_order.html', locals(),                                
                              context_instance=RequestContext(request) ) 



# ORDER_SUBFORMS = [ dof.OrderInfo, dof.Cabinetry, dof.Hardware, dof.Mouldings, dof.CabinetBoxes, 
#                     dof.CornerCabinetOptions, dof.IslandAndPeninsula, dof.OtherConsiderations,
#                     dof.SpaceManagement, dof.Miscellaneous, dof.FloorPlanDiagram ]
# #                    dof.SpaceManagement, dof.Miscellaneous, dof.Appliances  ]
ORDER_SUBFORMS = [ wf.ManufacturerForm, wf.HardwareForm, wf.MouldingForm, wf.SoffitsForm, 
                    wf.DimensionsForm, wf.CornerCabinetForm, wf.InteriorsForm, 
                    wf.MiscellaneousForm, wf.ApplianceForm, wf.AttachmentForm ]
                    # wf.MiscellaneousForm,  ]

# little util to help with form processing
def process_form(form_class, order_inst, data=None, files=None, model_class=WorkingOrder):
    # some of the forms need to always be instantiated unbound, and will be in 
    model = form_class._meta.model
    modelmatch = model == model_class
    if modelmatch:
        inst = order_inst
    else:
        inst = model()                
    if data or files:
        form = form_class(data, files, instance=inst )
        if form.is_valid():
            obj = form.save(commit=False)      
            obj.order = order_inst
            obj.save()            
    else:
        form = form_class(instance=inst)  

    if modelmatch:
        return (None, form)
    else:
        name = '%s_form' % model.__name__.lower() 
        return (name, form)

def edit_order_detail(request, order_id):
    """
    Editable detailed design order display. 

    This view constructs a set of subforms based on current order.    

    We attempt to give the template some flexibility with respect to how to manage
    data entry by decomposing the field set of the design order into a number of subforms.

    We pass the following to the template:
     - request context (of course)
     - order: the current DesignOrder object
     - formlist: a list of form objects for the field groups that comprise a DesignOrder
    """    
    user = request.user
    if user is None or not user.is_authenticated():
        return HttpResponseRedirect('/')
 
    profile = user.get_profile()
    account = profile.account.dealerorganization
    # order = account.created_orders.get(id=order_id)  # will throw if current user didn't create current order
    order = user.workingorder_set.get(id=order_id)  # will throw if current user didn't create current order
                        
    # if this is an update, determine which subform to apply and validate
    form_name = None
    if request.method == 'POST': 
        try:
            form_name = request.POST['_formname']
        except:
            raise IllegalStateException('Invalid form: missing required data!')   
                     
    formlist = []
    context = RequestContext(request)  
         
    for form_class in ORDER_SUBFORMS:
        if form_name and form_class.name == form_name:
            name,obj = process_form(form_class, order, request.POST, request.FILES)            
        else:
            name,obj = process_form(form_class, order) 
            
        if name:
            context[name] = obj
        else:
            formlist.append(obj)

    # context control...
    context['order'] = order
    context['formlist'] = formlist
    
    return render_to_response( "home/dealer_order_detail.html", context_instance=context )
    
        
def accept_floorplan_template_upload(request, orderid):
    pass
    

def accept_floorplan_template_fax(request, orderid):
    pass
    
    
@transaction.commit_on_success
def dealer_submit_order(request, orderid):
    """
    Change the order status from CLIENT_EDITING to CLIENT_SUBMITTED, and notify waiters.
    
    TODO - error handling, logging, 
    """
    
    popup_error = None
    order = get_current_order(request, orderid)
    if order.attachments.filter(type__exact=Attachment.FLOORPLAN):
        account = request.user.get_profile().account.dealerorganization
        if account.credit_balance >= order.cost:
            ## TODO: transactions
            now = datetime.utcnow()

            cost = order.cost or Decimal()
            
            # update account
            account.credit_balance = account.credit_balance - cost
            account.save()   

            # update order
            order.save()
                        
            # update transction log
            tx = Transaction()
            tx.account = account
            tx.amount = cost
            tx.debit_or_credit = 'C'  
            tx.trans_type = 'C'
            tx.description = 'design credit purchase'
            tx.timestamp = now
            tx.save()                        
            
        else:
            return HttpResponse('Insufficient account credit to place order. \
              Press "[back]" then fund your account to enable order submission.') 
    else:
        ##TODO: identify errors
        return HttpResponse('Order is incomplete. \
              Press "[back]" to return to the order detail screen and verify floorplan is attached.')
              
              
    return HttpResponseRedirect( reverse('home.views.dealer_dashboard') )
    
    
def dealer_review_order(request, orderid):
    ##FIXME dup
    order = get_current_order(request, orderid)
    if request.method == "GET":
        form = DesignOrderAcceptanceForm(instance=order)
    elif request.method == "POST":
        form = DesignOrderAcceptanceForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect( reverse('home.views.dealer_dashboard') )
    else:
        raise Exception, 'Invalid HTTP operation %s' % request.method        
        
    return render_to_response( "home/design_rating_form.html", locals(),
        context_instance=RequestContext(request) )
    
def dealer_accept_order(request, orderid):
    order = get_current_order(request, orderid)
    if request.method == "GET":
        form = DesignOrderAcceptanceForm(instance=order)
    elif request.method == "POST":
        form = DesignOrderAcceptanceForm(request.POST,instance=order)
        if form.is_valid():
            order.status = -1
            order.closed = datetime.now()
            form.save()            
            return HttpResponseRedirect( reverse('home.views.dealer_dashboard') )
    else:
        raise Exception, 'Invalid HTTP operation %s' % request.method        
        
    return render_to_response( "home/design_rating_form.html", locals(),
        context_instance=RequestContext(request) )
    
def dealer_reject_order(request, orderid):
    ##FIXME dup
    order = get_current_order(request, orderid)
    if request.method == "GET":
        form = DesignOrderAcceptanceForm(instance=order)
    elif request.method == "POST":
        form = DesignOrderAcceptanceForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect( reverse('home.views.dealer_dashboard') )
    else:
        raise Exception, 'Invalid HTTP operation %s' % request.method        
        
    return render_to_response( "home/design_rating_form.html", locals(),
        context_instance=RequestContext(request) )
    
def generate_floorplan_template(request, orderid):
    """
    Generate a floorplan template, customized to the current user (dealer) and order.
    
    
    """    
    return _generate_floorplan_template(get_current_order(request, orderid))
    

def _generate_floorplan_template(order):    
    response = HttpResponse(mimetype='application/pdf')    

    response['Pragma'] = 'no-cache'    
    #response['Content-Disposition'] = 'inline; filename=ft-%04d.pdf' % order.id 
    
    print '++++++++++++++++++++++'
    import sys 
    print 'client = %s' % order.client_account.id
    print 'order = %s' % order.id
    print '++++++++++++++++++++++'
    
    from pdfGen import KitchenTemplatePdfPage
    template = KitchenTemplatePdfPage(str(order.client_account.id),str(order.id))
    template.save()
    response.write( template.pdfBuffer.getvalue() )
    
    return response
    
def remove_order_appliance(request, orderid, appliance_key):
    order = get_current_order(request, orderid)
    # verify appliance is child of order
    if request.method == "POST":
        try:
            appliance = order.appliances.get(pk=appliance_key)
            appliance.delete()
            appliance.save()
        except Appliance.DoesNotExist:
            raise RuntimeException('Appliance does not exist!')
    return HttpResponseRedirect( reverse('edit_order', args=[orderid]) )
    