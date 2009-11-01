from django.conf.urls.defaults import *

import paypal

urlpatterns = patterns('customer.views', 
    (r'^$', 'home'),
    
    (r'^login/$', 'do_login'),
    url(r'^logout/$', 'do_logout', name='do-logout'),
    url(r'^dealer/profile/complete$', 'create_profile', name='dealer-complete-profile'),
    
    url(r'^dealer/$', 'dealer_dashboard', name='dealer-dashboard'),
    
    # (r'^dealer/order/$', 'dealer_dashboard'),                       
    url(r'^dealer/order/new/$', 'create_order', name='new_order'),
    (r'^dealer/order/(\d+)/edit/$', 'edit_order_detail'),
    (r'^dealer/order/(\d+)/template/$', 'generate_floorplan_template'),
    (r'^dealer/order/(\d+)/submit/$', 'dealer_submit_order'),
    (r'^dealer/order/(\d+)/review/$', 'dealer_review_order'),
    (r'^dealer/order/(\d+)/accept/$', 'dealer_accept_order'),
    (r'^dealer/order/(\d+)/reject/$', 'dealer_reject_order'),                       
                       
    url(r'^dealer/order/(\d+)/appliance/(\d+)/delete/$', 
        'remove_order_appliance', 
        name='delete_order_appliance'),
        
    (r'^dealer/order/(\w+)/fax-cover/', 'current_order_info', {
        'template': 'notification/fax-cover.html',
        }, 
        'fax_cover')
)


##
## /dealer/{userid}
## /profile/{userid}
## /orders/{userid}
## /billing/{userid}
##
