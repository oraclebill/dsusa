from django import forms
from dsprovider.ordermgr import models
from dsprovider.ordermgr import widgets


class AssignDesignerForm(forms.ModelForm):

    designer = forms.CharField(max_length=100)

    class Meta:
        model = models.DesignOrder
        fields = ['designer']


class DateRangeForm(forms.Form):
    start = forms.DateField(widget=widgets.JQueryDatepicker, required=False)
    end = forms.DateField(widget=widgets.JQueryDatepicker, required=False)
