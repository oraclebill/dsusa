from django import forms

from models import DesignPackage


class NewForm(forms.ModelForm):
    class Meta:
        model = DesignPackage
        fields = ('kitfile', 'designer', 'notes',)

class UpdateForm(forms.ModelForm):
    class Meta:
        model = DesignPackage
        fields = ('designer', 'notes',)
                