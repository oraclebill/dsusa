##
import logging
from datetime import datetime, timedelta

from django.core.exceptions import PermissionDenied
from django.template import RequestContext
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import dsprovider.ordermgr.models as models
import dsprovider.ordermgr.forms as forms
from django.forms.models import modelform_factory

log = logging.getLogger('ordermgr.views')


@login_required
def dashboard(request):
    """
    Dashboard page for designers

    Display a list of orders related to this designer, combined with a list of unclaimed orders.
    """
    pending = models.KitchenDesignRequest.objects.filter(status=models.STATUS_NEW)

    working = models.KitchenDesignRequest.objects.filter(status=models.STATUS_ASSIGNED)

    completed = models.KitchenDesignRequest.objects.filter(status=models.STATUS_COMPLETED)

    return render_to_response('designer/dashboard.html', {
        'pending': pending,
        'working': working,
        'completed': completed,
    }, context_instance=RequestContext(request))


@login_required
def manage_orders(request):
    pass


@login_required
def manage_designers(request):
    pass


@login_required
def manage_designer(request):
    pass

OPTIONAL_FIELD_NAMES = [ 
     'soffits',
     'soffit_height',
     'soffit_width',
     'soffit_depth',
     'stacked_staggered',
     'wall_cabinet_height',
     'vanity_cabinet_height',
     'vanity_cabinet_depth',
     'base_corner_cabinet',
     'base_corner_cabinet_opening',
     'base_corner_cabinet_shelving',
     'wall_corner_cabinet',
     'wall_corner_cabinet_opening',
     'wall_corner_cabinet_shelving',
     'island_peninsula_option',
     'countertop_option',
     'backsplash',
     'toekick',
     'lazy_susan',
     'slide_out_trays',
     'waste_bin',
     'wine_rack',
     'plate_rack',
     'appliance_garage',
     'corbels_brackets',
     'valance',
     'legs_feet',
     'glass_doors',
     'range_hood' ]

@login_required
def display_order(request, orderid, form_class=None):
    """
    Display a read-only view of the design request order, intended for designers.

    TODO: Printer CSS
    """
    order = get_object_or_404(models.KitchenDesignRequest, pk=orderid)

    form_class = form_class or modelform_factory(order.__class__)
    
    # disable assignment for non-new orders
    if not order.status == models.STATUS_NEW:
        assign_disabled='disabled="disabled"'
    else:
        assign_disabled=''
        
    # disable completion for non-assigned orders
    if not order.status == models.STATUS_ASSIGNED:
        complete_disabled='disabled="disabled"'
    else:
        complete_disabled=''

    errors = None
    # setup forms
    if request.method== 'GET':
        package_form = form_class(instance=order)
    elif request.method == 'POST':
        # use presence of FILES to distinguish between design update and 'complete' actions
        if request.FILES:
            package_form = form_class(request.POST, request.FILES, instance=order)
            if package_form.is_valid():
                package_form.save()
        else:
            # determine action type
            if 'complete-order-action' in request.POST:
                if order.package:
                    order.complete(request.user)
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

    
    optional_fields = [order._meta.get_field(f) for f in OPTIONAL_FIELD_NAMES ]
    
    # render template
    return render_to_response(
                'designer/display_order.html', {
                    'order': order,
                    'options': optional_fields,
                    'assign_disabled': assign_disabled,
                    'complete_disabled': complete_disabled,
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
def assign_designer_to_order(request, orderid, form_class=forms.AssignDesignerForm):
    """
    Create an order assignment by presenting a list of available (only?) designers for selection
    """
    # get/validate selected order is unassinged (new)
    order = get_object_or_404(models.KitchenDesignRequest, pk=orderid)

    # make sure order is assignable
    if order.status == models.STATUS_ASSIGNED:
        log.error( 'Order %s is already assigned to %s - cannot reassign' % (orderid, order.designer) )
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
            log.warning('assign_designer_to_order: unexpected state - invalid form' )
    else:
        log.error('invalid HTTP method in assign_designer_to_order: %s' % request.method )
        raise Exception, "Invalid request type %s" % request.method

    return render_to_response('designer/assign_order.html', locals(),
                context_instance=RequestContext(request) )

@login_required
def clarify_order(request, orderid):
    raise NotImplementedError("ordermgr.views.clarify_order is not implemented")


@login_required
def complete_order(request, orderid, form_class=None):

    # get/validate selected order is unassinged (new)
    order = get_object_or_404(models.KitchenDesignRequest, pk=orderid)

    form_class = forms.DesignFileForm

    errors = []
    try:
        package = models.DesignPackage.objects.get(order=order)            
    except:
        package = None

    form = form_class()
    if request.method == 'GET':
 	form = form_class()
    elif request.method == 'POST':
        if 'complete-order-action' in request.POST:
            vform_class = modelform_factory(
                models.DesignPackage, fields=('notes',)
            )
            vform = vform_class(request.POST, instance=package)
            if vform.is_valid():
                package = vform.save(commit=False)
                package.order=order
                package.save()            
            
                if package.kitfile and package.price_report:
                    if order.color_views: 
                        if package.views_archive:
                            order.complete(request.user)
                            return redirect(dashboard)                           
                        else:
                            errors = 'Order requires Views Package (ZIP)'
                    else:
                        order.complete(request.user)
                        return redirect(dashboard)                     
                else:
                    errors = 'Order requires KIT file and Price Report'      
        if 'upload-file-action' in request.POST:
            form = form_class(request.POST, request.FILES)
            if form.is_valid():
                ftype = form.cleaned_data['ftype']
                if not package:
                    package = models.DesignPackage(order=order)
                if ftype == forms.PRICE_REPORT:
                    package.price_report = form.cleaned_data['file']
                elif ftype == forms.KITFILE:
                    package.kitfile = form.cleaned_data['file']
                elif ftype == forms.VIEWS_ZIP:
                    package.views_archive = form.cleaned_data['file']
                package.save()
    # render template
    return render_to_response('designer/attach_design.html', locals(),
                context_instance=RequestContext(request) )

@login_required
def submit_order(request, orderid):
    pass


@login_required
def stats(request, queryset=None, field='completed',
        template_name='designer/stats_page.html', extra_context=None):
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

    context = {
        'form': forms.DateRangeForm(initial={
            'start': start_date,
            'end': end_date,
        }),
        'sum': sum([o.cost for o in qs]),
        'start_date': start_date,
        'end_date': end_date,
        'orders': qs,
        'query': request.META['QUERY_STRING'],
    }

    if extra_context:
        for key, value in extra_context.items():
            if callable(value):
                value = value()
            context[key] = value
    return render_to_response(template_name, context,
                              context_instance=RequestContext(request))
