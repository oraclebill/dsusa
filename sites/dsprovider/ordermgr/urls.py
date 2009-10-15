from django.conf.urls.defaults import *

urlpatterns = patterns('ordermgr.views',
        url(r'^$', 'dashboard', name='dashboard'),
        url(r'^order/(\d+)/display/$', 'display_order',
            name='order_detail'),

        url(r'^order/(\d+)/assign/$', 'assign_order',
            name='order_assign'),

        url(r'^order/(\d+)/claim/$', 'claim_order',
            name='order_claim'),

        url(r'^order/(\d+)/clarify/$', 'clarify_order',
            name='order_clarify'),

        url(r'^order/(\d+)/attach/$', 'attach_design_to_order',
            name='order_attach'),

        url(r'^order/(\d+)/complete/$', 'complete_order',
            name='order_complete'),

        url(r'^stats/$', 'stats', name="order_stats"),
)

urlpatterns += patterns('django.contrib.auth',
        url(r'^accounts/login/$', 'views.login', {
                'template_name': 'login.html',
        }, name='auth_login'),
        url(r'^accounts/logout/$', 'views.logout', name='auth_logout'),
)
