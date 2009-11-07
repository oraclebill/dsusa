from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

import designfirst.menus

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

# import customer.forms

urlpatterns = patterns('',
    (r'', include("customer.urls")),    
    (r'^products/', include("product.urls")),    
    (r'^orders/',   include("orders.urls")),
    (r'^accounts/', include('registration.urls')),
    (r'^barcode/',  include("barcode.urls")),        
    (r'^notification/',  include("notification.urls")),        
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/',    include(admin.site.urls)),
)

from django.conf import settings
if settings.DEBUG and settings.LOCAL:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
