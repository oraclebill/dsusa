from django import forms
from django.contrib.auth.models import User
from dsprovider.ordermgr import models


class AssignDesignerForm(forms.ModelForm):

    designer = forms.ModelChoiceField(
        queryset=User.objects.filter(is_staff=False, is_active=True))

    class Meta:
        model = models.DesignOrder
        fields = ['designer']


