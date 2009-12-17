from django.conf.urls.defaults import *

urlpatterns = patterns('orders.views',
    url(r'^(\d+)/print/$', 'print_order',  name='print-order'),
    #FIXME: hack: change the url to that it can't be confused with a wizard step.. 
    #url(r'^(?P<orderid>\d+)/delete/\?(?P<return_to>.*)$', 'delete_order', name='delete-order'),
    url(r'^delete/(?P<orderid>\d+)/$', 'delete_order', {'return_to': '/dealer/' }, name='delete-order'),

    url(r'^print/(\w+)/fax-cover/', 'print_order', {'template': 'orders/fax-cover.html', 'include_summary': False}, name='fax-cover'),

    url(r'^new/$', 'create_order', name='new_order'),
    url(r'^display/(\d+)/$', 'review_order', name='generic-order-review'),

    url(r'^complete/(\d+)/$', 'submit_order', name='submit-order'), # e.g. checkout
    url(r'^complete/(\d+)/details/$', 'post_submission_details', name='submit-order-completed'), # e.g. checkout acknowledgement
    
    url(r'^ajax/wood/$', 'ajax_wood',               name='ajax-door-material'),
    url(r'^ajax/manufacturer/$', 'ajax_manufacturer',               name='ajax-manufacturer'),
    url(r'^ajax/door/$', 'ajax_door_style',         name='ajax-door-style'),
    url(r'^ajax/finish_color/$', 'ajax_finish_color',     name='ajax-finish-color'),
    url(r'ajax/attachment/(\d+)/$', 'ajax_attach_details', name='ajax-attachment-details'),
    
    url(r'^(\d+)/([^/]+)/$', 'wizard', name='order-wizard-step'),
    url(r'^(\d+)/$', 'wizard', name='order-wizard'),
    
)
