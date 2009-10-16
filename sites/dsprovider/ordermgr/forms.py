from django import forms
from dsprovider.ordermgr import models
from dsprovider.ordermgr import widgets
from django.db.models import ObjectDoesNotExist


class AssignDesignerForm(forms.ModelForm):

    designer = forms.CharField(max_length=100)

    class Meta:
        model = models.DesignOrder
        fields = ['designer']


class DateRangeForm(forms.Form):
    start = forms.DateField(widget=widgets.JQueryDatepicker, required=False)
    end = forms.DateField(widget=widgets.JQueryDatepicker, required=False)


class KitchenOrderForm(forms.ModelForm):

    class Meta:
        model = models.KitchenDesignRequest
        exclude = ('arrived', 'status', 'id')

    def save(self, commit=True):
        obj = super(KitchenOrderForm, self).save(commit=False)
        id = '%s-%s' % (obj.source, obj.source_id)

        def id_taken(s):
            try:
                models.KitchenDesignRequest.objects.get(id=s)
            except ObjectDoesNotExist:
                return False
            return True

        if id_taken(id):
            counter = 1
            while id_taken('%s-%s' % (id, counter)):
                counter += 1

        obj.id = id
        if commit:
            obj.save()

        return obj
