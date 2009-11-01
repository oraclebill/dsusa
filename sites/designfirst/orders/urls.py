from django.conf.urls.defaults import *

urlpatterns = patterns('orders.views',
    url(r'^(\d+)/$', 'orders', name='order-orders'),
    url(r'^(\d+)/(.*?)/$', 'orders', name='order-wizard-step'),
    url(r'^complete/(\d+)/$', 'orders', {'complete': True}, name='order-wizard-complete'),
    url(r'^print/(\d+)/$', 'print_order', name='print-order'),
    
    url(r'^ajax/door/$', 'ajax_door_style', name='ajax-door-style'),
    url(r'^ajax/wood/$', 'ajax_wood', name='ajax-wood'),
    url(r'^ajax/finish_color/$', 'ajax_finish', name='ajax-finish_color'),
    url(r'ajax/attachment/(\d+)/$', 'ajax_attach_details', name='ajax-attachment-details')
)
