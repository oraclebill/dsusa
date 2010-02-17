from django.conf.urls.defaults import *

from views import *

urlpatterns = patterns('',
    url(r'^new/$',                  create_package,             name='create-package'),
    url(r'^(?P<packageid>\d+)/$',   update_package,             name='update-package'),
    url(r'^(\d+)/files/$',          list_package_files,         name='package-files-list'),
    url(r'^(\d+)/files/new/$',      upload_package_files,       name='package-files-upload'),
#    url(r'^(\d+)/files/(\d+)/$',    create_package,     name='package-file'),
#    url(r'^(\d+)/files/(\d+)/delete/$',  create_package, name='package-file-delete'),
    
#    url(r'^/?$', package_list, name='package-list'),
#    url(r'^(\d+)/$', package_detail, name='package-detail'),
#    url(r'^upload/$',  upload_handler, name='upload-handler'),
)

