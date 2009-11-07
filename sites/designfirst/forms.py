from django import forms
from django.db.models import ObjectDoesNotExist
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import force_unicode
import registration.forms
from home import models


attrs_dict = {'class': 'required'}


def organization_field(name, **kwargs):
    return models.DealerOrganization._meta.get_field(name).formfield(**kwargs)


def value_as_key(choices):
    return tuple([(c, c) for c in choices])


class RegistrationForm(forms.ModelForm):
    first_name = forms.CharField(label=('First name'), max_length=120)
    last_name = forms.CharField(label=('Last name'), max_length=120)
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
                                                               maxlength=75)),
                             label=_(u'Email address'))

    rush = forms.BooleanField(label=_('Rush My Signup!'), required=False)

    product_type = forms.ChoiceField(
        label=_("Prefered design product type"),
        widget=forms.widgets.RadioSelect,
        choices=value_as_key([
            'Pro Design - 20/20 .KIT File plus cabinet quote report.',
            'Presentation Pack - 20/20 file plus printable full-color perspective views, floorplan and cabinet elevations, and cabinet quote report (retail).',
            'Not sure.',
        ]),
    )

    revisions = forms.ChoiceField(
        label=_('How many revisions do you typically produce for a customer?'),
        widget=forms.widgets.RadioSelect,
        choices=value_as_key([
            'One - the first one usually does it',
            'Two - the original plus a touch up',
            'Three - the original and two updates',
            'Four or more',
        ]),
    )

    expected_orders = forms.DecimalField(required=False,
        label=_('Expected orders per month'),
    )

    class Meta:
        model = models.DealerOrganization
        exclude = ('status', 'credit_balance', 'default_measure_units', 'company_email')

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
        organization = super(RegistrationForm, self).save()

        notes='\n'.join([
            '%s: %s' % (force_unicode(self.fields[field].label), self.cleaned_data[field])
            for field in ('rush', 'product_type', 'revisions', 'expected_orders' )
        ])

        profile = models.UserProfile(
            first_name = self.cleaned_data['first_name'],
            last_name = self.cleaned_data['last_name'],
            email=self.cleaned_data['email'],
            notes=notes,
            account=organization)
        profile.save()

        registration_profile = registration.models.RegistrationProfile.objects.create_profile(
            related_object=profile,
        )

        registration.models.RegistrationProfile.objects.send_registered_email(
            registration_profile
        )

        return registration_profile


class CompanyProfileForm(forms.ModelForm):

    class Meta:
        model = models.DealerOrganization
        exclude = ('status', 'credit_balance', '')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = models.UserProfile
        exclude = ('user', 'notes', 'usertype', 'account')
