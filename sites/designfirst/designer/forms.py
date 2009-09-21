from django import forms
from home.models import DesignOrder

class DesignPackageUploadForm(forms.ModelForm):
    class Meta:
        model = DesignOrder
        fields = ['designer_package', 'designer_package_notes', 'designer_notes']

class DesignClarificationForm(forms.ModelForm):
    class Meta:
        model = DesignOrder
        fields = ['designer_notes']

    