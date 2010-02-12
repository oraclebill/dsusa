from django.conf.urls.defaults import *

from views import create_package, upload_files

package_files= upload_files

urlpatterns = patterns('',
    url(r'^new/$',                  create_package,     name='create-package'),
    url(r'^(\d+)/files/$',          package_files,      name='package-files'),
    url(r'^(\d+)/files/new/$',      upload_files,       name='package-file-upload'),
    url(r'^(\d+)/files/(\d+)/$',    create_package,     name='package-file'),
    url(r'^(\d+)/files/(\d+)/delete/$',  create_package, name='package-file-delete'),
    
#    url(r'^/?$', package_list, name='package-list'),
#    url(r'^(\d+)/$', package_detail, name='package-detail'),
#    url(r'^upload/$',  upload_handler, name='upload-handler'),
)

