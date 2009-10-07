from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, ImproperlyConfigured
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required

from models import UserProfile
from models import KitchenDesignRequest as DesignOrder
from models import STATUS_NEW, STATUS_ASSIGNED, STATUS_COMPLETED

import logging
log = logging.getLogger('ordermgr.views')


def get_context(request, orderid=None):
    user = request.user
    account = None
    profile = None
    order = None
    if user.is_authenticated():
        try:
            profile = user.get_profile()
        except UserProfile.DoesNotExist:
            profile = UserProfile(user=user)
            profile.save()
        # account = profile.account.designerorganization
        if orderid:
            try:
                order = DesignOrder.objects.get(pk=orderid)
            except ObjectDoesNotExist as ex:
                log.error( "failed to find the orderid %d" % orderid )
                raise ImproperlyConfigured("Access to order %s denied to user %s" % (orderid, user))
    else:
        log.error( "unathenticated user in get_context" )
        raise PermissionDenied()

    return (user, account, profile, order)


@login_required
def dashboard(request):
    """
    Dashboard page for designers

    Display a list of orders related to this designer, combined with a list of unclaimed orders.
    """
    user, account, profile, product = get_context(request)

    pending = DesignOrder.objects.filter(status=STATUS_NEW)

    working = DesignOrder.objects.filter(status=STATUS_ASSIGNED)

    completed = DesignOrder.objects.filter(status=STATUS_COMPLETED)
    # except:
    #     orders = []

    stats = { 'headers': ['Today', 'This Week', 'This Month'],
              'arrived': [3, 25, 84],
              'completed': [4, 22, 80],
            }

    return render_to_response( 'designer/dashboard.html', {
        'account': account,
        'pending': pending,
        'working': working,
        'completed': completed,
        'stats': stats,
    }, context_instance=RequestContext(request) )


@login_required
def manage_orders(request):
    pass

@login_required
def manage_designers(request):
    pass

@login_required
def manage_designer(request):
    pass


@login_required
def display_order(request, orderid):
    """
    Display a read-only view of the design request order, intended for designers.

    TODO: Printer CSS
    """
    # validate access
    user, account, profile, order = get_context(request, orderid)
    # disable control if not yet assigned
    if not order.status == STATUS_ASSIGNED:
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
                if order.package:
                    order.complete(user)
                    return redirect('ordermgr.views.dashboard')
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
                'designer/display_order.html', {
                    'order':order,
                    'options':order.display_as_optional,
                    'disabled':disabled,
                },
                context_instance=RequestContext(request) )


@login_required
def claim_order(request, orderid):
    """
    Claim an order for the current (logged in) designer.
    """

    # get authenticated user (designer)
    user, account, profile, order = get_context(request,orderid)

    if order and not order.is_assigned():
        order.assign_designer( user )
    else:
        log.error( 'Order %s is already assigned to %s - cannot reassign' % (orderid, user) )
        raise Exception, 'Order %s is already assigned to %s - cannot reassign' % (orderid, user)

    return redirect('ordermgr.views.dashboard')


@login_required
def assign_order(request, orderid):
    """
    Create an order assignment by presenting a list of available (only?) designers for selection
    """
    # get/validate selected order is unassinged (new)
    user, account, profile, order = get_context(request,orderid)
    # make sure user has right to assign orders
    if not user.is_staff:
        log.info('assign_order: assign order permission denied for user %s' % user )
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
            return redirect('ordermgr.views.dashboard')
        else:
            log.warning('assign_order: unexpected state - invalid form' )
    else:
        log.error('invalid HTTP method in assign_order: %s' % request.method )
        raise Exception, "Invalid request type %s" % request.method

    return render_to_response('designer/assign_order.html', locals(),
                context_instance=RequestContext(request) )

@login_required
def clarify_order(request,orderid):
    pass

@login_required
def attach_design_to_order(request,orderid):

    # get/validate selected order is unassinged (new)
    user, account, profile, order = get_context(request,orderid)
    #
    attachments = order.orderattachment_set.filter(source__exact=1)
    if request.method == 'GET':
        form = PackageForm()
    elif request.method == 'POST':
        form = PackageForm(request.POST,request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.order = order
            doc.source = 1
            doc.method = 0
            doc.user = user
            doc.org = account
            doc.save()
            return redirect(display_order, args=[orderid])
    else:
        log.error('Invalid HTTP method in attach_design_to_order: %s' % request.method )
        raise Exception, "Invalid request type %s" % request.method

    # render template
    return render_to_response('designer/attach_design.html', locals(),
                context_instance=RequestContext(request) )

@login_required
def submit_order(request, orderid):
    pass

@login_required
def complete_order(request, orderid):
    # get/validate selected order is unassinged (new)
    user, account, profile, order = get_context(request,orderid)
    try:
        order.complete(user)
        return redirect(dashboard)
    except:
        return redirect(request.META['HTTP_REFERER'])
