from django.conf.urls.defaults import *

urlpatterns = patterns('ordermgr.views',
        url(r'^$', 'dashboard', name='dashboard'),
        url(r'^order/(\w+)/display/$', 'display_order',
            name='order_detail'),

        url(r'^order/(\w+)/assign/$', 'assign_order',
            name='assign_order'),

        url(r'^order/(\w+)/claim/$', 'claim_order',
            name='order_claim'),

        url(r'^order/(\w+)/clarify/$', 'clarify_order',
            name='order_clarify'),

        url(r'^order/(\w+)/attach/$', 'attach_design_to_order',
            name='order_attach'),

        url(r'^order/(\w+)/complete/$', 'complete_order',
            name='order_complete'),

        url(r'^stats/$', 'stats', name="order_stats"),
)

