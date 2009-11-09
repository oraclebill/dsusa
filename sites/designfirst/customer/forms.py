from django import forms
from django.contrib.auth.models import User

from customer.models import Dealer, UserProfile
from product.models import Product

from orders.models import WorkingOrder


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
        profile_org = Dealer(
                        legal_name=self.cleaned_data['company'], 
                        address_1=self.cleaned_data['address'], 
                        city=self.cleaned_data['city'], 
                        state=self.cleaned_data['state'], 
                        zip4=self.cleaned_data['zip'], 
                        phone=self.cleaned_data['phone'], 
                        email=self.instance.email)

        profile_org.save()
        profile = UserProfile(
                        user=profile_user, 
                        account=profile_org, 
                        )
        profile.save()    
        return profile_user
    
class NewDesignOrderForm(forms.ModelForm):
    class Meta: 
        model = WorkingOrder
        fields = ['project_name', 'design_product', 'rush', 'client_notes']
    
    design_product = forms.ModelChoiceField(queryset=Product.objects.filter(debitable=True))
    

class DesignOrderAcceptanceForm(forms.Form):
    rating = forms.IntegerField()
    comments = forms.CharField(widget=forms.Textarea)
    
class DesignOrderRejectionForm(forms.Form):
    reason = forms.CharField(widget=forms.Textarea)
