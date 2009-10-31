from django.conf.urls.defaults import *

import paypal

urlpatterns = patterns('home.views', 
    (r'^$', 'home'),
    
    (r'^login/$', 'do_login'),
    url(r'^logout/$', 'do_logout', name='do-logout'),
    url(r'^dealer/profile/complete$', 'create_profile', name='dealer-complete-profile'),
    
    url(r'^dealer/$', 'dealer_dashboard', name='dealer-dashboard'),
    
    # (r'^dealer/order/$', 'views.dealer_dashboard'),                       
    url(r'^dealer/order/new/$', 'views.create_order', name='new_order'),
    (r'^dealer/order/(\d+)/edit/$', 'views.edit_order_detail'),
    (r'^dealer/order/(\d+)/template/$', 'views.generate_floorplan_template'),
    (r'^dealer/order/(\d+)/submit/$', 'views.dealer_submit_order'),
    (r'^dealer/order/(\d+)/review/$', 'views.dealer_review_order'),
    (r'^dealer/order/(\d+)/accept/$', 'views.dealer_accept_order'),
    (r'^dealer/order/(\d+)/reject/$', 'views.dealer_reject_order'),                       
                       
    url(r'^dealer/order/(\d+)/appliance/(\d+)/delete/$', 
        'remove_order_appliance', 
        name='delete_order_appliance'),
)


##
## /dealer/{userid}
## /profile/{userid}
## /orders/{userid}
## /billing/{userid}
##
