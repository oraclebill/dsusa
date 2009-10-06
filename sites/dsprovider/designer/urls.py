from django.conf.urls.defaults import *

urlpatterns = patterns('designer', 
                        (r'^$', 'views.designer_dashboard'),
                        (r'^order/(\d+)/display$', 'views.designer_display_order'),
                        (r'^order/(\d+)/assign$', 'views.designer_assign_order'),
                        (r'^order/(\d+)/claim$', 'views.designer_claim_order'),
                        (r'^order/(\d+)/clarify$', 'views.designer_clarify_order'),
                        (r'^order/(\d+)/attach$', 'views.designer_attach_design_to_order'),
                        (r'^order/(\d+)/complete$', 'views.designer_complete_order'),
                        (r'^login/$', 'views.designer_login'),
                        (r'^logout/$', 'views.designer_logout'),
                       )

