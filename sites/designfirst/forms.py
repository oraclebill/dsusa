from django import forms
from django.db.models import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
import registration.forms
from home import models


attrs_dict = {'class': 'required'}


def organization_field(name, **kwargs):
    return models.DealerOrganization._meta.get_field(name).formfield(**kwargs)


class RegistrationForm(forms.ModelForm):
    username = forms.RegexField(regex=r'^\w+$',
                                max_length=30,
                                widget=forms.TextInput(attrs=attrs_dict),
                                label=_(u'username'))
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_(u'email address'))
    first_name = forms.CharField(label=('First name'), max_length=120)
    last_name = forms.CharField(label=('Last name'), max_length=120)
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'password'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),
                                label=_(u'password (again)'))

    redirect_to = forms.CharField(widget=forms.HiddenInput, required=False)
    product_type = organization_field('product_type', widget=forms.widgets.RadioSelect)
    revisions = organization_field('revisions', widget=forms.widgets.RadioSelect)

    class Meta:
        model = models.DealerOrganization
        exclude = ('status', )

    def clean_username(self):
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['username'])
        except ObjectDoesNotExist:
            return self.cleaned_data['username']
        raise forms.ValidationError(_(u'This username is already taken. Please choose another.'))

    def clean(self):
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError(_(u'You must type the same password each time'))
        return self.cleaned_data

    def save(self):
        new_user = registration.models.RegistrationProfile.objects.create_inactive_user(username=self.cleaned_data['username'],
                                                                    password=self.cleaned_data['password1'],
                                                                    email=self.cleaned_data['email'],
                                                                    redirect_to=self.cleaned_data.get('redirect_to'))
        organization = super(RegistrationForm, self).save()
        profile = models.UserProfile(user=new_user, account=organization)
        profile.save()

        new_user.first_name = self.cleaned_data['first_name']
        new_user.last_name = self.cleaned_data['last_name']
        new_user.save()

        return new_user
