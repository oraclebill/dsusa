from django.db import models
from piston.handler import BaseHandler
from piston.utils import rc
from piston.utils import validate

from ordermgr.models import DesignOrder, KitchenDesignRequest
from ordermgr.forms import KitchenOrderForm


class OrderHandler(BaseHandler):
    """
    Authenticated entrypoint for orders.
    """
    model = DesignOrder
    fields = ('id', 'source', 'source_id', 'arrived')


class KitchenRequestHandler(BaseHandler):
    model = KitchenDesignRequest

    @validate(KitchenOrderForm, 'POST')
    def create(self, request):
        return super(OrderHandler, self).save(self, request)

