from django import forms
from customer.models import *
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
                        legal_name=self.cleaned_data['company'], 
                        address_1=self.cleaned_data['address'], 
                        city=self.cleaned_data['city'], 
                        state=self.cleaned_data['state'], 
                        zip4=self.cleaned_data['zip'], 
                        phone=self.cleaned_data['phone'], 
                        email=self.instance.email,
                        default_measure_units=INCH_DIMENSION)
        profile_org.save()
        profile = UserProfile(
                        user=profile_user, 
                        account=profile_org, 
                        usertype='dealer'
                        )
        profile.save()    
        return profile_user
    
class NewDesignOrderForm(forms.ModelForm):
    class Meta: 
        model = WorkingOrder
        fields = ['project_name', 'design_product', 'rush', 'client_notes']
    
    design_product = forms.ModelChoiceField(queryset=Product.objects.filter(debitable=True))
    

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
