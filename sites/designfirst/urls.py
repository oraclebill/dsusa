from django.conf.urls.defaults import *
from django.contrib.auth import views as auth_views
from django.views.generic.list_detail import object_detail
from django.views.generic.simple import direct_to_template

import menus  # remove this import and any page with a {% menu ... %} tag fails.. pretty damn random.. 

import uploadifytest

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'', include("customer.urls")),    
    (r'^accounts/', include("customer.registration.urls")),    
    (r'^products/', include("product.urls")),    
    (r'^orders/',   include("orders.urls")),
    (r'^barcode/',  include("barcode.urls")),        
    (r'^notification/',  include("notification.urls")),        
    (r'^support/',  'django.views.generic.simple.redirect_to', 
        {'url': 'http://www.designserviceusa.com/support' }, 'support'),
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/',    include(admin.site.urls)),
    
    # uploadify (obviously) 
    (r'^uploadify/', include('uploadify.urls')),
    (r'^uploadifytest1/', uploadifytest.view1), 
    (r'^uploadifytest2/', uploadifytest.view2), 
    (r'^uploadifytestcomplete/', uploadifytest.com_view, {}, 'upload_complete_url' ),    
)

# site housekeeping patterns
urlpatterns += patterns('',
    url(r'^pending/$', direct_to_template,  { 'template': 'account_pending.html' }, name='account-pending'),
    url(r'^suspended/$', direct_to_template,  { 'template': 'account_suspended.html' }, name='account-suspended'),
    url(r'^inactive/$', direct_to_template,   { 'template': 'account_inactive.html' }, name='account-inactive'),
    url(r'^denied/$', direct_to_template,     { 'template': 'access_denied.html' }, name='access-denied'),
)


from django.conf import settings
if settings.LOCAL:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
        (r'^files/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.APP_FILES_ROOT}),
    )
