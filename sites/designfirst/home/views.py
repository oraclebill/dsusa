import logging as log
from datetime import datetime, timedelta

from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User


from home import ACCOUNT_ID, ORDER_ID
from home.models import DealerAccount, DesignOrder, Transaction, OrderAppliance, \
    OrderDiagram   
#from home.forms import DesignOrderForm, DesignOrderDiagramForm
from forms import DesignOrderAcceptanceForm, NewDesignOrderForm 
from home import designorderforms as dof
from product.models import Product
from django.utils import simplejson



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
        order = account.created_orders.get(id=orderid)
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
            profile = user.get_profile()
            if profile is None:
                raise Exception("No profile")
                
            usertype = profile.usertype
            request.session[ACCOUNT_ID] = profile.account.id
            
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
    
    
def register(request):
    """
    Self serve registration process.
    
    TODO - implement
    """
    
    return render_to_response( 'home/registration.html',
                context_instance=RequestContext(request) )
    
    
def dealer_dashboard(request):
    """
    Display summary information for areas of dealer interest, provide primary navigation to work areas.
    
    TODO - document
    """
    
    user = request.user
    if user is None or not user.is_authenticated():
        return HttpResponseRedirect('/')
    
    account = request.user.get_profile().account.dealeraccount
    
    orders = account.created_orders.all()
    transactions = account.transaction_set.all()
    
    open_orders = orders.filter( Q(status='DLR') | Q(status='RCL') | Q(status='CMP') )
    working_orders = orders.filter( Q(status='ASG') | Q(status='SUB') )
    archived_orders = orders.filter( Q(status='ACC') | Q(status='REJ') | Q(status='WTH') )
        
    return render_to_response( 'home/dealer_dashboard.html', locals(),                                
                                context_instance=RequestContext(request) ) 
 

def create_order(request, *args):
    """
    Create a new order.
    """
    account = request.user.get_profile().account.dealeraccount              
    if request.method == 'POST':
        form = NewDesignOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.client_account = account
            order.save()
            
            request.session[ORDER_ID] = order.id#TODO: vitaliy: for what is this? 
            
            return HttpResponseRedirect( reverse( "home.views.edit_order_detail", args=[order.id] ) )
    else:
        desired = (datetime.now() + timedelta(days=2))
        form = NewDesignOrderForm(initial={'desired': desired, 'cost':None})
    
    #Prices is used to get price from product when user switches product in from
    prices = dict([(p.id, float(p.customer_price(account))) 
                   for p in Product.objects.all()])
    prices = simplejson.dumps(prices)
    return render_to_response('home/create_order.html', locals(),                                
                              context_instance=RequestContext(request) ) 



ORDER_SUBFORMS = [ dof.OrderInfo, dof.Cabinetry, dof.Hardware, dof.Mouldings, dof.CabinetBoxes, 
                    dof.CornerCabinetOptions, dof.IslandAndPeninsula, dof.OtherConsiderations,
                    dof.SpaceManagement, dof.Miscellaneous, dof.FloorPlanDiagram ]
#                    dof.SpaceManagement, dof.Miscellaneous, dof.Appliances  ]

def edit_order_detail(request, order_id):
    """
    Editable detailed design order display. 

    This view
        - validates login
        - gets the current working order from session / db
        - constructs as set of subforms based on current order.    

    We attempt to give the template some flexibility with respect to how to manage
    data entry by decomposing the field set of the design order into a number of subforms.

    Based on the form_id in post request we update the 'visited_status' of the order 
    to note the corresponding field group has been visited. 

    We pass the following to the template:
     - request context (of course)
     - order: the current DesignOrder object
     - formlist: a list of form objects for the field groups that comprise a DesignOrder
         Each field group (form) has some additional properties just for enhancing 
         display processing:
            - status: ('valid'|'invalid') based on form.is_valid
            - visited: ('visited'|'') based on bitset check in order.visited_status
            - current: True if it was the form posted on last request, false otherwise
    """    

    user = request.user
    if user is None or not user.is_authenticated():
        return HttpResponseRedirect('/')
 
    profile = user.get_profile()
    account = profile.account.dealeraccount
    order = account.created_orders.get(id=order_id)  # will throw if current user didn't create current order

    if order.submitted is not None:
        raise Exception("Invalid Operation - can't edit submitted order")

    posted_id = None
    subforms = []
    
    ApplianceFormSet = modelformset_factory(OrderAppliance, extra=1) 
    
    appliance_forms = None
    
    file_upload = [None]
    
    def add_subform(form, selected_id=None):
        form.validity = form.is_valid() and 'valid' or 'invalid'
        form.visited = ((1<<form.id) & order.visited_status) and 'visited' or ''
        form.current = (form.id == selected_id) 
        
        if form.id != dof.FloorPlanDiagram.id:
            subforms.append( form )
        else:
            file_upload[0] = form
                    

    # if this is a get initialize order subforms for display
    if request.method == 'GET':
        
        appliance_forms = ApplianceFormSet(queryset=order.orderappliance_set.all())

        for form in ORDER_SUBFORMS:
            subform = form(instance=order)
            add_subform( subform )
        
    # if this is an update, determine which subform to apply and validate
    elif request.method == 'POST': 

        try:
            posted_id = request.POST['subform']
        except:
            posted_id = '-1'
            
        posted_id = int( posted_id )
        posted_subform = None        
        
        for form_class in ORDER_SUBFORMS:
            if form_class.id == posted_id:
                form = form_class(request.POST, request.FILES, instance=order)
                posted_subform = form
                order.visited_status |= 1<<form.id
            else:
                form = form_class(instance=order)              
        
            log.debug("in loop(a), form.(name/id) = %s/%s" % (form.name, form.id) )

            add_subform( form, posted_id )
            
                    
        if not posted_subform: 
            # posted form was not in list,
            # so it's  appliance formset             
                
            appliance_forms = ApplianceFormSet(request.POST, queryset=order.orderappliance_set.all())
            if appliance_forms and appliance_forms.is_valid():            
                instances = appliance_forms.save(commit=False)
                for instance in instances:  
                    instance.order_id = order.id                
                    instance.save()                    
    	else:
            appliance_forms = ApplianceFormSet(queryset=order.orderappliance_set.all())
            if posted_subform.is_valid():
                if request.FILES:
                    order.client_diagram_source = 'UPL'  
                posted_subform.save()     

    # otherwise choke
    else:
        raise "unsupported http method"

    return render_to_response( "home/dealer_order_detail.html", 
        dict( order=order, formlist=subforms, formset=appliance_forms, file_upload=file_upload[0]  ),
        context_instance=RequestContext(request) )
    
        
def accept_floorplan_template_upload(request, orderid):
    pass
    

def accept_floorplan_template_fax(request, orderid):
    pass
    
    
def dealer_submit_order(request, orderid):
    """
    Change the order status from CLIENT_EDITING to CLIENT_SUBMITTED, and notify waiters.
    
    TODO - error handling, logging, 
    """
    
    popup_error = None
    order = get_current_order(request, orderid)
    if order.is_submittable():
        account = request.user.get_profile().account.dealeraccount
        if account.credit_balance >= order.cost:
            ## TODO: transactions
            now = datetime.utcnow()

            # update account
            account.credit_balance = account.credit_balance - order.cost     
            account.save()   

            # update order
            order.dealer_submit()
                        
            # update transction log
            tx = Transaction()
            tx.account = account
            tx.amount = order.cost
            tx.debit_or_credti = 'C'  
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
              Press "[back]" to return to the order detail screen.')
              
              
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
            order.status = 'ACC'
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
    
