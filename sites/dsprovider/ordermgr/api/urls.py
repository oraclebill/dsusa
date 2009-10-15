from django.conf.urls.defaults import *
from piston.resource import Resource
from piston import authentication as auth
from piston import doc
from ordermgr.api import handlers

authentication = auth.HttpBasicAuthentication()

orders = Resource(handler=handlers.OrderHandler,
                     authentication=authentication)

kitchens = Resource(handler=handlers.KitchenRequestHandler,
                     authentication=authentication)

urlpatterns = patterns('',
    url(r'^order/$', orders, name="orders"),
    url(r'^kitchen/$', kitchens, name="kitchens"),
    url(r'^$', doc.documentation_view),
)
