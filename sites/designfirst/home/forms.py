from django import forms
from home.models import *
from product.models import Product
import designorderforms
from wizard.models import WorkingOrder
# from designorderforms import *


class DealerProfileForm(forms.ModelForm):
    company = forms.CharField(max_length=75)
    address = forms.CharField(max_length=75)
    city = forms.CharField(max_length=30)
    state = forms.CharField(max_length=2)
    zip  = forms.CharField(max_length=10)
    phone = forms.CharField(max_length=15)
        
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'email' ]
        
    def save(self, **kwargs):
        profile_user = self.instance
        super(DealerProfileForm, self).save(**kwargs)
        profile_org = DealerOrganization(
                        company_name=self.cleaned_data['company'], 
                        company_address_1=self.cleaned_data['address'], 
                        company_city=self.cleaned_data['city'], 
                        company_state=self.cleaned_data['state'], 
                        company_zip4=self.cleaned_data['zip'], 
                        company_phone=self.cleaned_data['phone'], 
                        company_email=self.instance.email,
                        default_measure_units=INCH_DIMENSION)
        profile_org.save()
        profile = UserProfile(
                        user=profile_user, 
                        account=profile_org, 
                        usertype='dealer'
                        )
        profile.save()    
        return profile_user
    
class DesignOrderForm(forms.ModelForm):
    class Meta: 
        model = DesignOrder
        fields = ( 'customer', 'received', 'project_name', 'design_type', 
                'color_views', 'elevations', 'price_report', 'addl_notification_method',
                'desired', 'document_reference_id', 'source', 'entered_by', )
    
    def __init__(self, *args, **kwargs):
        # if initialized, make some fields readonly and disabled...
        i = kwargs['initial']
        for f in ('customer', 'source', 'entered_by'):
            if f in i:               
                self.base_fields[f].widget.attrs['readonly'] = True
                self.base_fields[f].widget.attrs['disabled'] = True
        super(DesignOrderForm, self).__init__(*args, **kwargs)   

class NewDesignOrderForm(forms.ModelForm):
    cost = forms.CharField(widget=forms.TextInput(attrs={'readonly':'true'}))
    class Meta: 
        model = WorkingOrder
        fields = ['project_name', 'desired', 'cost', 'client_notes']
    
    design_product = forms.ModelChoiceField(queryset=Product.objects.filter(debitable=True))
    
    def __init__(self, *args, **kwargs):
        #changing order of the fields
        self.base_fields.keyOrder = ['project_name', 'design_product', 'desired', 'cost', 'client_notes']
        self.base_fields['client_notes'].label = 'Notes'
        super(NewDesignOrderForm, self).__init__(*args, **kwargs)   

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
