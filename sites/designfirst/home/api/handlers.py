from piston.handler import BaseHandler
from piston import utils

from home import models as home_models
from home import forms


class DesignPackageHandler(BaseHandler):
    allowed_methods = ('POST', )
    model = home_models.DesignOrder
    fields = ('project_name', 'description', 'status')

    def create(self, request):
        form = forms.DesignPackageForm(request.POST, request.FILES)
        if form.is_valid():
            order = form.cleaned_data['order']
            order.add_package(
                form.cleaned_data['upload'],
                form.cleaned_data['notes'])
            return order
        raise utils.FormValidationError(form)

