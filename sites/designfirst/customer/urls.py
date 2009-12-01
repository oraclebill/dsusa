from django.conf.urls.defaults import *

import paypal

from models import Invoice

urlpatterns = patterns('customer.views', 
    (r'^$', 'home'),    

    url(r'^dealer/profile/complete$', 'edit_profile', name='dealer-complete-profile'),
    url(r'^dealer/profile/$', 'edit_profile', name='profile-edit'),
    
    url(r'^dealer/$', 'dealer_dashboard', name='home'),
    
    (r'^dealer/order/(\d+)/edit/$', 'edit_order_detail'),
    (r'^dealer/order/(\d+)/submit/$', 'dealer_submit_order'),
#    (r'^dealer/order/(\d+)/review/$', 'dealer_review_order'),
    (r'^dealer/order/(\d+)/accept/$', 'dealer_accept_order'),
    (r'^dealer/order/(\d+)/reject/$', 'dealer_reject_order'),                       
                       
    url(r'^dealer/order/(\d+)/appliance/(\d+)/delete/$', 
        'remove_order_appliance', 
        name='delete_order_appliance'),
        
    url(r'^dealer/order/(\w+)/fax-cover/', 'current_order_info', name='fax_cover'),
    
    url(r'^dealer/invoice/(\d+)/$', 'display_invoice', name='display-invoice'),
    
)

# invoice display
invoice_params = { 'queryset': Invoice.objects.all() }                           
urlpatterns += patterns('',
    url(r'^dealer/invoice/$', 'customer.views.invoice_list', invoice_params, name='invoice-list'),
    url(r'^dealer/invoice/(?P<object_id>\w+)/$', 'django.views.generic.list_detail.object_detail', invoice_params, name='invoice-detail'),
)

# misc
urlpatterns += patterns('',
    url(r'access-denied/$', 'django.views.generic.simple.direct_to_template', {
        'template': 'customer/access_denied.html',
    }, name='customer_access_denied'),
)

##
## /dealer/{userid}
## /profile/{userid}
## /orders/{userid}
## /billing/{userid}
##
