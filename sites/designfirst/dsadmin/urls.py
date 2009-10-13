from django.conf.urls.defaults import *
from django.views.generic import list_detail 
from home.models import DealerOrganization, DesignOrder

confirm_attrs = {
    'queryset': DesignOrder.objects.all(),
    'template_name': 'dsadmin/orders/new_order_confirmation.html',    
}

urlpatterns = patterns( 'dsadmin.views', 

    # admin section home
    url(r'^$', 'dashboard', name='dsadmin-dashboard'),

    # account urls
    url(r'^accounts/$', 
        list_detail.object_list, 
        { 'queryset': DealerOrganization.objects.all(), } ) ,
        
    url(r'^accounts/verify_customer/$', 
        'verify_customer', 
        name='verify-new-customer'),
    
    # order management urls
    url(r'^/orders/newfax/$', 
        'process_fax_order', 
        name='process-fax-order'),
        
    url(r'^/orders/(?P<object_id>\d+)/confirmation$', 
        list_detail.object_detail, confirm_attrs,
        name='new-order-confirmation'),
        
    url(r'^orders/(?P<orderid>\d+)/edit/$', 
        'edit_fax_order', 
        name='edit-fax-order'),
        
    url(r'^orders/(?P<orderid>\d+)/attach/$', 
        'attach_faxed_floorplan', 
        name='attach-order-floorplan'),
        
    url(r'^orders/(?P<orderid>\d+)/fulfill/$', 
        'process_design_response', 
        name='process-design-response'),    
)


