from django.conf.urls.defaults import *

import paypal

from models import Invoice

urlpatterns = patterns('customer.views', 
    (r'^$', 'home'),    #TODO: cleanup urlconf duplication
                        #TODO: localize 'dealer' urlconf

    url(r'^dealer/profile/complete$', 'edit_profile', name='dealer-complete-profile'),
    url(r'^dealer/profile/$', 'edit_profile', name='profile-edit'),
    
    url(r'^dealer/$', 'dealer_dashboard', name='dealer-dashboard'),
    
    (r'^dealer/order/(\d+)/accept/$', 'dealer_accept_order'),
    (r'^dealer/order/(\d+)/reject/$', 'dealer_reject_order'),                       
                           
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
