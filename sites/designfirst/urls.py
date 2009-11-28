from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import permission_required
from django.views.generic.list_detail import object_detail
from django.views.generic.simple import direct_to_template


import menus  # remove this import and any page with a {% menu ... %} tag fails.. pretty damn random.. 

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'', include("customer.urls")),    
    (r'^accounts/', include("customer.registration.urls")),    
    (r'^products/', include("product.urls")),    
    (r'^orders/',   include("orders.urls")),
    (r'^barcode/',  include("barcode.urls")),        
    (r'^notification/',  include("notification.urls")),        
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/',    include(admin.site.urls)),
)

from django.conf import settings
if settings.DEBUG and settings.LOCAL:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.APP_FILES_ROOT}),
    )
