import logging

from django.core.exceptions import PermissionDenied, ObjectDoesNotExist, ImproperlyConfigured
from datetime import datetime, timedelta
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect
from django.contrib.auth.decorators import login_required
import dsprovider.ordermgr.models as models
import dsprovider.ordermgr.forms as forms
from django.forms.models import modelform_factory

log = logging.getLogger('ordermgr.views')

def get_context(request, orderid=None):
    user = request.user
    account = None
    profile = None
    order = None
    if user.is_authenticated():
        profile = user.get_profile()
        # account = profile.account.designerorganization
        if orderid:
            try:
                order = models.KitchenDesignRequest.objects.get(pk=orderid)
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

    pending = models.KitchenDesignRequest.objects.filter(status=models.STATUS_NEW)

    working = models.KitchenDesignRequest.objects.filter(status=models.STATUS_ASSIGNED)

    completed = models.KitchenDesignRequest.objects.filter(status=models.STATUS_COMPLETED)

    return render_to_response( 'designer/dashboard.html', {
        'account': account,
        'pending': pending,
        'working': working,
        'completed': completed,
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
def display_order(request, orderid, form_class=None):
    """
    Display a read-only view of the design request order, intended for designers.

    TODO: Printer CSS
    """
    # validate access
    user, account, profile, order = get_context(request, orderid)
    form_class = form_class or modelform_factory(order.__class__)
    # disable control if not yet assigned
    if not order.status == models.STATUS_ASSIGNED:
        disabled='disabled="disabled"'
    else:
        disabled=''

    errors = None
    # setup forms
    if request.method== 'GET':
        package_form = form_class(instance=order)
    elif request.method == 'POST':
        # use presence of FILES to distinguish between design update and 'complete' actions
        if request.FILES:
            package_form = form_class(request.POST,request.FILES,instance=order)
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
                    # 'options':order.display_as_optional,
                    'disabled':disabled,
                },
                context_instance=RequestContext(request) )


@login_required
def claim_order(request, orderid):
    """
    Claim an order for the current (logged in) designer.
    """
    raise NotImplementedError("Designers can't log in site yet.")

    # get authenticated user (designer)
    # user, account, profile, order = get_context(request,orderid)

    # if order and not order.status == models.STATUS_ASSIGNED:
    #     order.assign_designer(user)
    # else:
    #     log.error( 'Order %s is already assigned to %s - cannot reassign' % (orderid, user) )
    #     raise Exception, 'Order %s is already assigned to %s - cannot reassign' % (orderid, user)

    # return redirect('ordermgr.views.dashboard')


@login_required
def assign_order(request, orderid, form_class=forms.AssignDesignerForm):
    """
    Create an order assignment by presenting a list of available (only?) designers for selection
    """
    # get/validate selected order is unassinged (new)
    user, account, profile, order = get_context(request,orderid)
    # make sure order is assignable
    if order.status == models.STATUS_ASSIGNED:
        log.error( 'Order %s is already assigned to %s - cannot reassign' % (orderid, designer) )
        raise PermissionDenied

    # display designers eligible for assignment
    # TODO: filter out assigned designers...
    if request.method == 'GET':
        form = form_class(instance=order)
    elif request.method == 'POST':
        form = form_class(request.POST, instance=order)
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
    raise NotImplementedError("ordermgr.views.clarify_order is not implemented")

@login_required
def attach_design_to_order(request,orderid, form_class=None):

    # get/validate selected order is unassinged (new)
    user, account, profile, order = get_context(request, orderid)
    #
    form_class = form_class or modelform_factory(
        models.CompletedDesignFile, exclude=('order', 'delivered')
    )

    #this should be orderattachment class or something like that
    attachments = order.attachments.all()
    if request.method == 'GET':
        form = form_class()
    elif request.method == 'POST':
        form = form_class(request.POST,request.FILES)
        if form.is_valid():
            doc = form.save(commit=False)
            doc.order = order
            # doc.source = 1
            # doc.method = 0
            # doc.user = user
            # doc.org = account
            doc.save()
            return redirect(order)
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


@login_required
def stats(request, queryset=None, field='completed'):
    """
    Shows stats for completed orders over a period of time.
    """
    qs = queryset or models.DesignOrder.objects.filter(
                                            status=models.STATUS_COMPLETED)

    form = forms.DateRangeForm(request.GET)
    if form.is_valid():
        start_date = form.cleaned_data['start']
        end_date = form.cleaned_data['end']
    else:
        start_date, end_date = None, None

    if not start_date and not end_date:
        # last  two weeks by default
        today = datetime.today()
        start_date = today - timedelta(datetime.weekday(today) + 7)
        end_date = today

    if start_date:
        qs = qs.filter(**{'%s__gte' % field: start_date})
    if end_date:
        qs = qs.filter(**{'%s__lte' % field: end_date})

    return render_to_response("designer/stats_page.html", {
        'form': forms.DateRangeForm(initial={
            'start': start_date,
            'end': end_date,
        }),
        'start_date': start_date,
        'end_date': end_date,
        'orders': qs,
    }, context_instance=RequestContext(request))
