from django.conf.urls.defaults import *
from designfirst import home

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^designfirst/', include('designfirst.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'', include("home.urls")),    
    (r'^designer/', include("designer.urls")),
    (r'^products/', include("product.urls")),

    (r'^admin/', include(admin.site.urls)),

    (r'^60b9f188a8a27ce69fcba9ee63b74b4e2fad2b3d/', include('paypal.standard.ipn.urls')),

)


from django.conf import settings
if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )