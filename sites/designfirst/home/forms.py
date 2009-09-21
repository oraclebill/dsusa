from django import forms
from home.models import *
import designorderforms
# from designorderforms import *

class DesignOrderForm(forms.ModelForm):
    class Meta: 
        model = DesignOrder
        exclude = [ 'id', 'client_account', 'visited_status', 'valid_status', 'designer',
            'designer_package', 'designer_package_notes', 'designer_notes', 'modified', 
            'modified_by', 'created', 'submitted', 'assigned', 'completed', 'closed', 
            'tracking_notes' ]
        

class DesignOrderAppliancesForm(forms.ModelForm):
    class Meta: 
        model = OrderAppliance
        exclude = [ 'order' ]

class DesignOrderDiagramForm(forms.ModelForm):
    class Meta: 
        model = OrderDiagram
        exclude = [ 'order' ]

class DesignOrderAcceptanceForm(forms.ModelForm):
    class Meta: 
        model = DesignOrder
        fields = [ 'client_review_rating', 'client_review_notes' ]

class DesignOrderRejectionForm(forms.ModelForm):
    class Meta: 
        model = DesignOrder
        fields = [ 'client_review_notes' ]
