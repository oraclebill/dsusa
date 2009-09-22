# Create your views here.
from datetime import datetime 

from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.forms.models import modelformset_factory
from django.template import RequestContext

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User

from django.shortcuts import render_to_response

from home import ACCOUNT_ID
from home.models import DesignOrder
from designer.models import DesignerAccount
from designer.forms import DesignPackageUploadForm as PackageForm
from designer.forms import AssignDesignerForm

import logging
log = logging.getLogger('designer.views')


def get_designer_context(request, orderid=None):
    user = request.user
    account = None
    profile = None
    order = None
    if user.is_authenticated():
        profile = user.get_profile()
        account = profile.account.designeraccount
        if orderid:
            try:
                order = DesignOrder.objects.get(pk=orderid)
            except ObjectDoesNotExist as ex: 
                log.error( "failed to find the orderid %d" % orderid )
                raise ImproperlyConfigured("Access to order %s denied to user %s" % (orderid, user))
    else:
        log.error( "unathenticated user in get_designer_context" )
        raise PermissionDenied()
    
    return (user, account, profile, order)


def designer_login(request):
    """
    Log a designer in. 
    
    Maintain a separate view so the login screen can look a little different.
    """
    
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            profile = user.get_profile()
            if profile is None:
                raise "No profile"
            usertype = profile.usertype
            if usertype == 'dealer':            
                request.session[ACCOUNT_ID] = profile.account.id
            elif usertype == 'designer':
                request.session[DESIGNER_ID] = profile.designer.id
            return HttpResponseRedirect( '/%s/' % usertype )
        else:
            return render_to_response('home/home.html', 
                dict(login_message="User is locked. Please contact support"),
                context_instance=RequestContext(request))
    else:
        return render_to_response('home/home.html', dict(login_message="Login failed."),
            context_instance=RequestContext(request))



def designer_logout(request):
    """
    Log a designer out. 
    
    Maintain a separate view so the logout screen can look a little different.
    """
    raise Exception("UNIMPLEMENTED")



def designer_dashboard(request):
    """
    Dashboard page for designers
    
    Display a list of orders related to this designer, combined with a list of unclaimed orders.
    """
    user,account,profile,product = get_designer_context(request)
    
    pending = DesignOrder.objects.filter( Q(designer__isnull=True) | 
        Q(designer=account), Q(submitted__isnull=False), Q(status='SUB')  )
        
    working = DesignOrder.objects.filter( status='ASG' )
    
    completed = DesignOrder.objects.filter( status='CMP' )
    # except:
    #     orders = []
        
    stats = { 'headers': ['Today', 'This Week', 'This Month'], 
              'arrived': [3, 25, 84],
              'completed': [4, 22, 80],
            }
            
    return render_to_response( 'designer/designer_dashboard.html', 
                            { 'account':account, 'pending':pending, 'working': working, 
                              'completed': completed, 'stats':stats },
                            context_instance=RequestContext(request) ) 


def designer_manage_orders(request):
    pass
    
def designer_manage_designers(request):
    pass
    
def designer_manage_designer(request):
    pass
        
            
def designer_display_order(request, orderid):
    """
    Display a read-only view of the design request order, intended for designers.
    
    TODO: Printer CSS    
    """    
    # validate access
    user, account, profile, order = get_designer_context(request,orderid)
    # disable control if not yet assigned
    if not hasattr(order.designer,'id') :
        disabled='disabled=disabled'
    else:
        disabled=''
    
    errors = None
    # setup forms
    if request.method== 'GET':
        package_form = PackageForm(instance=order) 
    elif request.method == 'POST':
        # use presence of FILES to distinguish between design update and 'complete' actions
        if request.FILES:
            package_form = PackageForm(request.POST,request.FILES,instance=order)
            if package_form.is_valid():
                package_form.save()
        else:
            # determine action type
            if 'complete-order-action' in request.POST:
                if order.designer_package:
                    order.designer_complete(user)
                    return HttpResponseRedirect(reverse('designer.views.designer_dashboard'))
                else:
                    log.warning( "Attempt to complete order without attached design(s)" )
                    errors = "Cannot complete design order without attached design package"
            elif 'clarify-order-action' in request.POST:
                # TODO: clarification request
                raise Exception, "Clarify Unimplemented!"
            elif 'attach-order-action' in request.POST:
                # TODO: attachment request
                raise Exception, "Attach Unimplemented!"
            else:
                log.error( "unknown form action: %s" % request.POST )
                raise Exception, "Unknown or unsupported action!"
    else:
        log.error( "Illegal HTTP Operation %s" % request.method )
        raise Exception, "Illegal HTTP Operation %s" % request.method
            
    # render template
    return render_to_response( 
                'designer/designer_display_order.html', { 
                    'order':order, 
                    'options':order.display_as_optional,
                    'disabled':disabled,
                }, 
                context_instance=RequestContext(request) )
    
def designer_claim_order(request, orderid):
    """
    Claim an order for the current (logged in) designer.
    """

    # get authenticated user (designer)
    user, account, profile, order = get_designer_context(request,orderid)

    if order and not order.is_assigned():
        order.assign_designer( user )
    else:
        log.error( 'Order %s is already assigned to %s - cannot reassign' % (orderid, user) )
        raise Exception, 'Order %s is already assigned to %s - cannot reassign' % (orderid, user)
            
    return HttpResponseRedirect(reverse('designer.views.designer_dashboard'))

def designer_assign_order(request, orderid ):
    """
    Create an order assignment by presenting a list of available (only?) designers for selection
    """    
    # get/validate selected order is unassinged (new)
    user, account, profile, order = get_designer_context(request,orderid)
    # make sure user has right to assign orders
    if not user.is_staff:
        log.info('designer_assign_order: assign order permission denied for user %s' % user )
        raise PermissionDenied
    # make sure order is assignable 
    if order.is_assigned():
        log.error( 'Order %s is already assigned to %s - cannot reassign' % (orderid, designer) )
        raise PermissionDenied

    # display designers eligible for assignment
    # TODO: filter out assigned designers...
    if request.method == 'GET':
        form = AssignDesignerForm(instance=order)
    elif request.method == 'POST':
        form = AssignDesignerForm(request.POST, instance=order)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.assign_designer(instance.designer) # designer was assigned by form..            
            return HttpResponseRedirect(reverse('designer.views.designer_dashboard'))
        else:
            log.warning('designer_assign_order: unexpected state - invalid form' )
    else:
        log.error('invalid HTTP method in designer_assign_order: %s' % request.method )
        raise Exception, "Invalid request type %s" % request.method

    return render_to_response('designer/designer_assign_order.html', locals(),                
                context_instance=RequestContext(request) )        

def designer_clarify_order(request,orderid):
    pass
    
def designer_attach_design_to_order(request,orderid):
    
    # get/validate selected order is unassinged (new)
    user, account, profile, order = get_designer_context(request,orderid)
    # 
    if request.method == 'GET':
        form = PackageForm(instance=order) 
    elif request.method == 'POST':
        form = PackageForm(request.POST,request.FILES,instance=order)
        if form.is_valid():
            form.save()
    else:
        log.error('Invalid HTTP method in designer_attach_design_to_order: %s' % request.method )
        raise Exception, "Invalid request type %s" % request.method
    
    # render template
    return render_to_response('designer/designer_attach_design.html', locals(),
                context_instance=RequestContext(request) )
            
def designer_submit_order(request, orderid):
    pass

def designer_complete_order(request, orderid):
    pass
