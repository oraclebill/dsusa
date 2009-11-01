from django.conf.urls.defaults import *

urlpatterns = patterns('barcode.views', 
    url(r'^(?P<type>c128|dmtx)/(?P<val>[\w-]+).png$', 'generate_barcode_response', name='generate_barcode'),
)
                    