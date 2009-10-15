from django.conf.urls.defaults import *
from piston.resource import Resource
from piston.authentication import NoAuthentication
from piston.doc import documentation_view
from ordermgr.api.handlers import OrderHandler

#TODO: authentication
orders = Resource(handler=OrderHandler,
                     authentication=NoAuthentication())

urlpatterns = patterns('',
    url(r'^order/$', orders, name="orders"),
    url(r'^kitchen/$', orders, name="kitchens"),

    # automated documentation
    url(r'^$', documentation_view),
)
