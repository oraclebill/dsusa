from django.conf.urls.defaults import *

urlpatterns = patterns('barcode.views', 
    url(r'^(\w+).png$', 'generate_barcode_response', name='generate_barcode'),
)
                    