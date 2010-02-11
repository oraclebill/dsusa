from django.conf.urls.defaults import *

urlpatterns = patterns('orders.views',
    url(r'^new/$', 'create_order', name='create-order'),
    url(r'^(?P<orderid>\d+)/delete/$', 'delete_order', {'return_to': '/dealer/' }, name='delete-order'),
    url(r'^(\d+)/$', 'review_order', name='generic-order-review'),
    url(r'^(\d+)/print/$', 'print_order',  name='print-order'),
    url(r'^(\d+)/edit/$', 'wizard', name='order-wizard'),
    url(r'^(\d+)/edit/([^/]+)/$', 'wizard', name='order-wizard-step'),
    url(r'^(\d+)/submit/$', 'submit_order', name='submit-order'), # e.g. checkout
    url(r'^(\d+)/submit/details/$', 'post_submission_details', name='submit-order-completed'), # e.g. checkout acknowledgement
    url(r'^(\d+)/complete/$', 'complete_order', name='complete-order'), 
    
    # dependent objects
    url(r'^(\d+)/attachments/$',                    'attachment_list',      name='order-attachments'), 
    url(r'^(\d+)/attachments/upload/$',             'attachment_upload',    name='order-attachment-upload'), 
#    url(r'^(\d+)/attachments/(\d+)/$',              'attachment',           name='order-attachment'), 
    url(r'^(\d+)/attachments/(\d+)/detail/$',       'attachment_details',   name='order-attachment-display'), 
    
    # TODO: fix
    url(r'^print/(\w+)/fax-cover/', 'print_order', {'template': 'orders/fax-cover.html', 'include_summary': False}, name='fax-cover'),

    # TODO: these should be catalog urls..
    url(r'^ajax/wood/$', 'ajax_wood', name='ajax-door-material'),
    url(r'^ajax/manufacturer/$', 'ajax_manufacturer', name='ajax-manufacturer'),
    url(r'^ajax/door/$', 'ajax_door_style', name='ajax-door-style'),
    url(r'^ajax/finish_color/$', 'ajax_finish_color', name='ajax-finish-color'),
    url(r'ajax/attachment/(\d+)/$', 'ajax_attach_details', name='ajax-attachment-details'),
    
    
)
