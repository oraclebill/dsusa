from customer import models
from django import forms
from django.utils.encoding import force_unicode
from django.utils.translation import ugettext_lazy as _
import registration


attrs_dict = {'class': 'required'}


#def organization_field(name, **kwargs):
#    return models.Dealer._meta.get_field(name).formfield(**kwargs)

def value_as_key(choices):
    return tuple([(c, c) for c in choices])


#class RegistrationForm(forms.ModelForm):
#    first_name = forms.CharField(label=('First name'), max_length=120)
#    last_name   = forms.CharField(label=('Last name'), max_length=120)
#    user_email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict,
#                                                               maxlength=75)),
#                             label=_(u'Email address'))
#
#    rush = forms.BooleanField(label=_('Rush My Signup!'), required=False)
#
#    product_type = forms.ChoiceField(
#        label=_("Prefered design product type"),
#        widget=forms.widgets.RadioSelect,
#        choices=value_as_key([
#            'Pro Design - 20/20 .KIT File plus cabinet quote report.',
#            'Presentation Pack - 20/20 file plus printable full-color perspective views, floorplan and cabinet elevations, and cabinet quote report (retail).',
#            'Not sure.',
#        ]),
#    )
#
#    revisions = forms.ChoiceField(
#        label=_('How many revisions do you typically produce for a customer?'),
#        widget=forms.widgets.RadioSelect,
#        choices=value_as_key([
#            'One - the first one usually does it',
#            'Two - the original plus a touch up',
#            'Three - the original and two updates',
#            'Four or more',
#        ]),
#    )
#
#    expected_orders = forms.DecimalField(required=False,
#        label=_('Expected orders per month'),
#    )
#
#    class Meta:
#        model = models.Dealer
#        exclude = ('status', 'credit_balance', 'default_measure_units', 'email', 'internal_name')
#
#    def save(self):
#        dealer = super(RegistrationForm, self).save(commit=False)
#
#        notes='\n'.join([
#            '%s: %s' % (force_unicode(self.fields[field].label), self.cleaned_data[field])
#            for field in ('rush', 'product_type', 'revisions', 'expected_orders' )
#        ])
#        dealer.notes = notes
#        dealer.status = dealer.PENDING
#        dealer.save()
#
#        profile = models.UserProfile(
#            first_name = self.cleaned_data['first_name'],
#            last_name = self.cleaned_data['last_name'],
#            email=self.cleaned_data['user_email'],
#            account=dealer)
#        profile.save()
#
#        registration_profile = registration.models.RegistrationProfile.objects.create_profile(
#            related_object=profile,
#        )
#
#        registration.models.RegistrationProfile.objects.send_registered_email(
#            registration_profile
#        )
#
#        return registration_profile

class CompanyProfileForm(forms.ModelForm):

    class Meta:
        model = models.Dealer
        exclude = ('status', 'credit_balance', 'internal_name')


class UserProfileForm(forms.ModelForm):

    class Meta:
        model = models.UserProfile
        exclude = ('user', 'notes', 'usertype', 'account', 'primary')
