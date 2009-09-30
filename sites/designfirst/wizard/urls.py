from django.conf.urls.defaults import *

urlpatterns = patterns('wizard.views',
    url(r'^(\d+)/$', 'wizard', name='order-wizard'),
    url(r'^(\d+)/(.*?)/$', 'wizard', name='order-wizard-step'),
    url(r'^complete/(\d+)/$', 'wizard', {'complete': True}, name='order-wizard-complete'),
    
    url(r'^ajax/door/$', 'ajax_door_style', name='ajax-door-style'),
    url(r'^ajax/wood/$', 'ajax_wood', name='ajax-wood'),
    url(r'^ajax/finish/$', 'ajax_finish', name='ajax-finish'),
)
