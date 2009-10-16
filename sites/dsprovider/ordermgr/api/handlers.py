from piston.handler import BaseHandler
from piston import utils

from ordermgr.models import DesignOrder, KitchenDesignRequest
from ordermgr.forms import KitchenOrderForm


class OrderHandler(BaseHandler):
    """
    Authenticated entrypoint for orders.
    """
    model = DesignOrder
    fields = ('id', 'source', 'source_id', 'arrived')
    exclude = ('final_type', 'id')
    allowed_methods = ('GET', )


class KitchenRequestHandler(BaseHandler):
    model = KitchenDesignRequest
    allowed_methods = ('POST', )

    # @utils.validate(KitchenOrderForm, 'POST')
    def create(self, request):
        form = KitchenOrderForm(request.POST, request.FILES)

        if not form.is_valid():
            raise utils.FormValidationError(form)


        attrs = self.flatten_dict(request.POST)
        try:
            inst = self.queryset(request).get(**attrs)
            return utils.rc.DUPLICATE_ENTRY
        except self.model.MultipleObjectsReturned:
            return utils.rc.DUPLICATE_ENTRY
        except self.model.DoesNotExist:
            pass

        return form.save()





