from django.conf.urls.defaults import *

urlpatterns = patterns('ordermgr',
        (r'^$', 'views.dashboard'),
        (r'^order/(\d+)/display$', 'views.display_order'),
        (r'^order/(\d+)/assign$', 'views.assign_order'),
        (r'^order/(\d+)/claim$', 'views.claim_order'),
        (r'^order/(\d+)/clarify$', 'views.clarify_order'),
        (r'^order/(\d+)/attach$', 'views.attach_design_to_order'),
        (r'^order/(\d+)/complete$', 'views.complete_order'),
)

urlpatterns += patterns('django.contrib.auth',
        url(r'^accounts/login/$', 'views.login', {
                'template_name': 'login.html',
        }, name='auth_login'),
        url(r'^accounts/logout/$', 'views.logout', name='auth_logout'),
)
