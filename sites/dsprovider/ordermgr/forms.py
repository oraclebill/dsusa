from django import forms
from django.contrib.auth.models import User
from dsprovider.ordermgr import models


class AssignDesignerForm(forms.ModelForm):

    # designer = forms.ModelChoiceField(
    #     queryset=User.objects.filter(is_staff=False, is_active=True))
    designer = forms.CharField(max_length=100)

    class Meta:
        model = models.DesignOrder
        fields = ['designer']


