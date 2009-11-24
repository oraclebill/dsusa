from django.conf.urls.defaults import *

urlpatterns = patterns('orders.views',
    url(r'^(\d+)/$', 'wizard', name='order-wizard'),
    url(r'^(\d+)/(.*?)/$', 'wizard', name='order-wizard-step'),
    url(r'^new/$', 'create_order', name='new_order'),
    url(r'^submit/(\d+)/$', 'submit_order', name='dealer_submit_order'),
    url(r'^review/(\d+)/$', 'review_order', name='generic-order-review'),
    url(r'^complete/(\d+)/$', 'wizard', {'complete': True}, name='order-wizard-complete'),
    url(r'^print/(\d+)/$', 'print_order', name='print-order'),
    
#     url(r'^ajax/line/$', 'ajax_product_line',         name='ajax-product-line'),
    url(r'^ajax/wood/$', 'ajax_wood',               name='ajax-door-material'),
    url(r'^ajax/door/$', 'ajax_door_style',         name='ajax-door-style'),
#     url(r'^ajax/drawer/$', 'ajax_drawer_style',       name='ajax-drawer-style'),
#     url(r'^ajax/finish_type/$',  'ajax_finish_type',  name='ajax-finish-type'),
    url(r'^ajax/finish_color/$', 'ajax_finish_color',     name='ajax-finish-color'),
#     url(r'^ajax/finish_options/$', 'ajax_finish_options',     name='ajax-finish-options'),
    
    url(r'ajax/attachment/(\d+)/$', 'ajax_attach_details', name='ajax-attachment-details')
)
