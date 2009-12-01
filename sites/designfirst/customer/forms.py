from django import forms
from django.db import transaction
from django.forms.models import model_to_dict
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _


from django.contrib.localflavor.us.forms import USPhoneNumberField, USStateField, USZipCodeField, USStateSelect


from customer.models import Dealer, UserProfile
from product.models import Product

from orders.models import WorkingOrder

class CompanyProfileForm(forms.ModelForm):

    class Meta:
        model = Dealer
        exclude = ('status', 'credit_balance', 'internal_name')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = UserProfile
        exclude = ('user', 'account', 'primary')


class DealerProfileForm(forms.ModelForm):
    legal_name = forms.CharField(label=_('Company Name'), max_length=75)
    address_1 = forms.CharField(label=_('Address'), max_length=75)
    address_2 = forms.CharField(label='', max_length=75, required=False)
    city = forms.CharField(max_length=30)
    state = USStateField(widget=USStateSelect)
    zip4  = USZipCodeField()
    phone = USPhoneNumberField()
        
    class Meta:
        model = User
        fields = [ 'first_name', 'last_name', 'email' ]
    
    def __init__(self, data=None, instance=None ):
        profile = instance.get_profile()
        if profile:
            initial = model_to_dict(profile.account, fields=['legal_name', 'address_1',  'address_2', 'city', 'state', 'zip4', 'phone'])
        super(DealerProfileForm,self).__init__(data=data, instance=instance, initial=initial)
                    
    @transaction.commit_on_success
    def save(self, **kwargs):
        profile_user = super(DealerProfileForm, self).save(**kwargs)        
        profile = profile_user.get_profile()
        if profile:
            profile_org = profile.account
        else:
            profile_org = Dealer()
              
        profile_org.legal_name=self.cleaned_data['legal_name'] 
        profile_org.address_1=self.cleaned_data['address_1'] 
        profile_org.city=self.cleaned_data['city']
        profile_org.state=self.cleaned_data['state'] 
        profile_org.zip4=self.cleaned_data['zip4']
        profile_org.phone=self.cleaned_data['phone'] 
        profile_org.email=self.instance.email
        profile_org.save()
        
        if not profile:
            profile = UserProfile(
                            user=profile_user, 
                            account=profile_org, 
                            )
            profile.save()    
        return profile_user
    
class DesignOrderAcceptanceForm(forms.Form):
    rating = forms.IntegerField()
    comments = forms.CharField(widget=forms.Textarea)
    
class DesignOrderRejectionForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea)
