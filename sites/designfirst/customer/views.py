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
from django.http import HttpResponseRedirect, HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.template import RequestContext
from django.shortcuts import render_to_response
from django.db.models import Q
from django.db import transaction

from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

## third party ##
from notification.models import NoticeType, NoticeSetting

## imports from other apps
from accounting.models import register_design_order
from product.models import Product
from orders.models  import BaseOrder, WorkingOrder, Appliance, Moulding, Attachment
##
## local imports 
from constants import ACCOUNT_ID, ORDER_ID
from models import Dealer, Invoice, UserProfile  
from django.core import context_processors
import forms
from forms import DesignOrderAcceptanceForm, DealerProfileForm


#TODO: need to be able to delete orders in dashboard

##
## UTILITY FUNCTIONS
##

def get_current_order(request, orderid):
    """
    Get an order object by id, validating that the current user has access.
    
    TODO
    """

    try:
        order = request.order_queryset.get(id=orderid)
    except:
        raise PermissionDenied("Access to orderid %d denied" % orderid)
    
    return order
    

##
## VIEW FUNCTIONS
##

def home(request):
    """
    Render the home page and clear current session.
    """    
    if request.session:
        request.session.flush()
    return HttpResponseRedirect(reverse('dealer-dashboard'))

def edit_profile(request, template='profiles/edit_profile.html', extra_context={}):
    """
    Display and edit user profile.
    
    Profile consists of:
         - user contact info
         - organization info (editable if user is primary contact)
         - notification preferences
    """
    user = request.user
    
    notice_types = NoticeType.objects.all()
    notice_settings = NoticeSetting.objects.filter(user=request.user)
    
    ns_queryset = NoticeSetting.objects.filter(user=request.user)
    if request.method == 'GET':
        form = DealerProfileForm(instance=user)
    else:
        if 'add-notification' in request.GET:
            #TODO: add
            pass                
        if 'delete-notification' in request.GET:
            # TODO: delete
            pass                
        if 'update-profile' in request.GET:            
            form = DealerProfileForm(request.POST, instance=user)
            if form.is_valid():
                form.save()
        else:
            form = DealerProfileForm(instance=user)
                    
    context = dict(account=request.account, form=form, notice_types=notice_types, notice_settings=notice_settings)
    context.update(extra_context)
    
    return render_to_response( template, context, context_instance=RequestContext(request))
                    
@login_required
def dealer_dashboard(request):
    """
    Display summary information for areas of dealer interest, provide primary navigation to work areas.
    
    TODO - document
    """
    
    if request.account:    
        orders = request.user.workingorder_set.all()
        invoices = request.account.invoice_set.order_by('-created')[:5]
    else:
        orders = WorkingOrder.objects.all()
        invoices = Invoice.objects.order_by('-created')[:5]
        
    
    working_orders = orders.filter( status__exact = BaseOrder.Const.DEALER_EDIT )
    submitted_orders = orders.filter( status__in = [ BaseOrder.Const.SUBMITTED, BaseOrder.Const.ASSIGNED ] )
        ## TODO: fixme!
    archived_orders = orders.exclude( status__in = [ BaseOrder.Const.DEALER_EDIT, BaseOrder.Const.SUBMITTED, BaseOrder.Const.ASSIGNED ] ) 
        
    return render_to_response( 'customer/dealer_dashboard.html', locals(),                                
                                context_instance=RequestContext(request) ) 

        
@login_required
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
            return HttpResponseRedirect( reverse('customer.views.dealer_dashboard') )
    else:
        raise Exception, 'Invalid HTTP operation %s' % request.method        
        
    return render_to_response( "customer/design_rating_form.html", locals(),
        context_instance=RequestContext(request) )
    
@login_required
def dealer_reject_order(request, orderid):
    ##FIXME dup
    order = get_current_order(request, orderid)
    if request.method == "GET":
        form = DesignOrderAcceptanceForm(instance=order)
    elif request.method == "POST":
        form = DesignOrderAcceptanceForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect( reverse('customer.views.dealer_dashboard') )
    else:
        raise Exception, 'Invalid HTTP operation %s' % request.method        
        
    return render_to_response( "customer/design_rating_form.html", locals(),
        context_instance=RequestContext(request) )
        
    
from django.views.generic.list_detail import object_list, object_detail
@login_required
def invoice_list(request, queryset):
    if request.account:
        queryset = queryset.filter(customer=request.account)
    elif not request.user.is_staff:
        return HttpResponseForbidden("2.1")
    return object_list(request,queryset)

@login_required
def display_invoice(request, queryset, object_id):
    if request.account:
        queryset = queryset.filter(customer=request.account)
    elif not request.user.is_staff:
        return HttpResponseForbidden("2.2")
    return object_detail(request,queryset,object_id=object_id)
