from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
)
urlpatterns += patterns('django.contrib.auth',
        url(r'^accounts/login/$', 'views.login', {
                'template_name': 'login.html',
        }, name='auth_login'),
        url(r'^accounts/logout/$', 'views.logout', {
        		'template_name': 'login.html',
		}, name='auth_logout'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
    )

urlpatterns += patterns('',
    (r'^', include("ordermgr.urls")),
)
