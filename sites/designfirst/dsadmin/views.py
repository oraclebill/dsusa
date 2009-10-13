# library imports 

# django imports
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect,\
    HttpResponseForbidden
from django.shortcuts import get_object_or_404
from django.utils import simplejson

# project imports
from home.forms import CreateOrderForm, EditOrderForm, \
    DealerProfileForm, DesignOrderAttachmentForm
from home.models import DealerOrganization, DesignOrder, OrderAttachment
from utils.views import render_to

@login_required 
@render_to('dsadmin/dashboard.html')
def dashboard(request):
    # list unverified customers
    pending_customers = DealerOrganization.objects.filter(
        status__exact=DealerOrganization.PENDING)
    # list pending/incomplete orders
    pending_orders = DesignOrder.objects.all() ## FIXME: limit orders to those requiring attentino 
    # list unprocessed designs    
    pending_designs = None ## FIXME: ?? 
    return locals()
    
@login_required 
@render_to('dsadmin/customer/verify.html')
def verify_customer(request):
    form_class = DealerProfileForm
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = form_class()
    return dict(form=form)  
    
   
@login_required 
@render_to('dsadmin/orders/process_fax_order.html')    
def process_fax_order(request):
    """
    Process an incoming fax order.
    
    Steps: 
        - use contents of fax cover to create order
        - transcribe design information into design request info
        - extract floorplan from fax and attach as floorplan-diag 
        - if sufficient account credit, 
            - email confirmation to customer, acct_rep
            - if beta, wait for acct_rep approval before sending to dsorg
        - if insufficient credit
            - email order-pending-credit message to customer, acct_rep
            - wait for credit and acct_rep approval to continue order
        - on approval email to oneworld
    """    
    form_class = CreateOrderForm
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            order = form.save()
            return HttpResponseRedirect(reverse('new-order-confirmation', args=[order.id]))            
    else:
        form = form_class()
    return dict(form=form)  

@login_required 
@render_to('dsadmin/orders/edit_fax_order.html')    
def edit_fax_order(request, orderid):
    """
    Process an incoming fax order.
    
    Steps: 
        - use contents of fax cover to create order
        - transcribe design information into design request info
        - extract floorplan from fax and attach as floorplan-diag 
        - if sufficient account credit, 
            - email confirmation to customer, acct_rep
            - if beta, wait for acct_rep approval before sending to dsorg
        - if insufficient credit
            - email order-pending-credit message to customer, acct_rep
            - wait for credit and acct_rep approval to continue order
        - on approval email to oneworld
    """
    form_class = EditOrderForm
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = form_class()
    return dict(form=form)  

@login_required 
@render_to('dsadmin/orders/add_faxed_diagram.html')    
def attach_faxed_floorplan(request, orderid):
    """
    Process an incoming PDF fax diagram.

    Faxed diagrams require some processing during attachment to ensure
    readability and to remove customer identifying information.
     
    Typically this consists of:
        - extracting desired pages (e.g. select page(s))
        - ensuring proper orientation (e.g. rotate)
        - removing fax markers (e.g. crop)
        - obscuring personal information (e.g. redact) 
        
    If a PNG/JPG image is uploaded it is assumed to be a preprocessed
    floorplan diagram and is attached directly.
    
    When a PDF file is uploaded it is split into pages and each 
    page is attached as an individual PNG file attachment.  
    """
    form_class = DesignOrderAttachmentForm
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = form_class()
    return dict(form=form)  

@login_required 
@render_to('dsadmin/orders/process_design_received.html')    
def process_design_response(request):
    form_class = EditOrderForm
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = form_class()
    return dict(form=form)  

@login_required 
@render_to('dsadmin/accounts/customer_list.html')    
def customer_list(request):
    form_class = EditOrderForm
    if request.method == 'POST':
        form = form_class(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = form_class()
    return dict(form=form)  

