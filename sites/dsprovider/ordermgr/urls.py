from django.conf.urls.defaults import *

urlpatterns = patterns('ordermgr',
        (r'^$', 'views.dashboard'),
        url(r'^order/(\d+)/display/$', 'views.display_order',
            name='order_detail'),

        url(r'^order/(\d+)/assign/$', 'views.assign_order',
            name='order_assign'),

        url(r'^order/(\d+)/claim/$', 'views.claim_order',
            name='order_claim'),

        url(r'^order/(\d+)/clarify/$', 'views.clarify_order',
            name='order_clarify'),

        url(r'^order/(\d+)/attach/$', 'views.attach_design_to_order',
            name='order_attach'),

        url(r'^order/(\d+)/complete/$', 'views.complete_order',
            name='order_complete'),
)

urlpatterns += patterns('django.contrib.auth',
        url(r'^accounts/login/$', 'views.login', {
                'template_name': 'login.html',
        }, name='auth_login'),
        url(r'^accounts/logout/$', 'views.logout', name='auth_logout'),
)
