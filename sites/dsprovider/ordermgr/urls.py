from datetime import datetime
from django.conf.urls.defaults import *

urlpatterns = patterns('ordermgr.views',
        url(r'^$', 'dashboard', name='dashboard'),

        url(r'^order/([\w-]+)/display/$', 'display_order',
            name='order_detail'),

        url(r'^order/([\w-]+)/assign/$', 'assign_designer_to_order',
            name='assign_designer_to_order'),

        url(r'^order/([\w-]+)/claim/$', 'claim_order',
            name='order_claim'),

        url(r'^order/([\w-]+)/clarify/$', 'clarify_order',
            name='order_clarify'),

        url(r'^order/([\w-]+)/complete/$', 'complete_order',
            name='complete_order_page'),

        url(r'^stats/$', 'stats', name="order_log"),

        url(r'^invoice/(?P<invoice_id>\d+)/$', 'invoice',
            name="order_invoice"),
        url(r'^invoice/(?P<invoice_id>\d+)/print/$', 'invoice', {
            'template_name': 'designer/invoice_print.html',
        }, name="order_invoice_print"),
        url(r'^invoice/create/$', 'create_invoice',
            name='order_invoice_create'),
        url(r'^invoice/$', 'invoice_list',
            name='order_invoice_list'),
)
