from django.conf.urls.defaults import *

from views import create_package

urlpatterns = patterns('',
    url(r'^new/$',  create_package, name='create_package'),
#    url(r'^/?$', package_list, name='package-list'),
#    url(r'^(\d+)/$', package_detail, name='package-detail'),
#    url(r'^upload/$',  upload_handler, name='upload-handler'),
)

