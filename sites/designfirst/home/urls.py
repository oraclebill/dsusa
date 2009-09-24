from django.conf.urls.defaults import *

import paypal

urlpatterns = patterns('home', 
    (r'^$', 'views.home'),
    
    (r'^login/$', 'views.do_login'),
    url(r'^logout/$', 'views.do_logout', name='do-logout'),
    (r'^register/$', 'views.register'),
    
    url(r'^dealer/$', 'views.dealer_dashboard', name='dealer-dashboard'),
    
    # (r'^dealer/order/$', 'views.dealer_dashboard'),                       
    (r'^dealer/order/new/$', 'views.create_order'),
    (r'^dealer/order/(\d+)/edit/$', 'views.edit_order_detail'),
    (r'^dealer/order/(\d+)/template/$', 'views.generate_floorplan_template'),
    (r'^dealer/order/(\d+)/submit/$', 'views.dealer_submit_order'),
    (r'^dealer/order/(\d+)/review/$', 'views.dealer_review_order'),
    (r'^dealer/order/(\d+)/accept/$', 'views.dealer_accept_order'),
    (r'^dealer/order/(\d+)/reject/$', 'views.dealer_reject_order'),                       
)


##
## /dealer/{userid}
## /profile/{userid}
## /orders/{userid}
## /billing/{userid}
##
