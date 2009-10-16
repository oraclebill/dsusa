from django.conf.urls.defaults import *
from piston import resource
from piston import authentication as auth
from piston import doc
from home.api import handlers

authentication = auth.HttpBasicAuthentication()

packages = resource.Resource(
    handler=handlers.DesignPackageHandler,
    authentication=authentication)

urlpatterns = patterns('',
    url(r'^packages/$', packages, name="packages"),
    url(r'^$', doc.documentation_view),
)
