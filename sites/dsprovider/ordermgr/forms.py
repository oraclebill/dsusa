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

KITFILE,  PRICE_REPORT, VIEWS_ZIP = ('kit', 'prices', 'views')
DESIGN_FILE_CHOICES = ((KITFILE, '20/20 KIT File'), (PRICE_REPORT, 'Cabinet Price Report'), (VIEWS_ZIP, 'PDF Views ZIP'))

class DesignFileForm(forms.Form):
    file = forms.FileField()
    ftype = forms.ChoiceField(choices=DESIGN_FILE_CHOICES)