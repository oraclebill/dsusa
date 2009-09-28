from django import forms
from home.models import *
from product.models import Product
import designorderforms
from wizard.models import WorkingOrder
# from designorderforms import *


class NewDesignOrderForm(forms.ModelForm):
    class Meta: 
        model = WorkingOrder
        fields = ['project_name', 'desired', 'cost', 'client_notes']
    
    design_product = forms.ModelChoiceField(queryset=Product.objects.all())
    
    def __init__(self, *args, **kwargs):
        #changing order of the fields
        self.base_fields.keyOrder = ['project_name', 'design_product', 'desired', 'cost', 'client_notes']
        self.base_fields['client_notes'].label = 'Notes'
        super(NewDesignOrderForm, self).__init__(*args, **kwargs)
    

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

class DesignOrderAttachmentForm(forms.ModelForm):
    class Meta: 
        model = OrderAttachment
        exclude = [ 'order' ]

class DesignOrderAcceptanceForm(forms.ModelForm):
    class Meta: 
        model = DesignOrder
        fields = [ 'client_review_rating', 'client_review_notes' ]

class DesignOrderRejectionForm(forms.ModelForm):
    class Meta: 
        model = DesignOrder
        fields = [ 'client_review_notes' ]
