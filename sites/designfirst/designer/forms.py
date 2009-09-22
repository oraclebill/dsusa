from django import forms
from django.contrib.auth.models import User

from home.models import DesignOrder

class DesignPackageUploadForm(forms.ModelForm):
    class Meta:
        model = DesignOrder
        # fields = ['designer_package', 'designer_package_notes', 'designer_notes']
        fields = ['designer_package']

class DesignClarificationForm(forms.ModelForm):
    class Meta:
        model = DesignOrder
        fields = ['designer_notes']

class AssignDesignerForm(forms.ModelForm):
    class Meta:
        model = DesignOrder
        fields = ['designer']    
        
    designer = forms.ModelChoiceField(
        queryset=User.objects.filter(userprofile__usertype__exact='designer'))
        