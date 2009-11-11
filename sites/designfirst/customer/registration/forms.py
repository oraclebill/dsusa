from django import forms
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.localflavor.us.forms import USPhoneNumberField, USStateField, USZipCodeField
from customer.models import Dealer

attrs_dict = { 'class': 'required' }

def value_as_key(choices):
    return tuple([(c, c) for c in choices])

class DealerRegistrationForm(forms.Form):
    # contact info
    first_name = forms.CharField(label=_('First'), max_length=30)
    last_name = forms.CharField(label=_('Last'), max_length=30)
    email = forms.EmailField(label=_('Email'))

    # business info
    legal_name = forms.CharField(label=_('Business Name'), max_length=50)
    address_1 = forms.CharField(label=_('Street Address'), max_length=40)
    address_2 = forms.CharField(label=_('Address Line 2'), max_length=40, required=False)
    city = forms.CharField(label=_('City'), max_length=20)
    state = USStateField(label=_('State / Province / Region'))
    zip4 = USZipCodeField(label=_('Zip / Postal Code'))
    phone = USPhoneNumberField(label=_('Phone'))
    fax = USPhoneNumberField(label=_('Fax'), required=False)
    account_rep_name = forms.CharField(label=_('Account Representative'), max_length=30)
    num_locations = forms.IntegerField(label=_('Number of Locations'), initial=1, required=False)

    # marketing info
    rush = forms.BooleanField(label=_('Rush My Signup!'), required=False)
    product_type = forms.ChoiceField(
        required = False,
        label=_("Prefered design product type"),
        widget=forms.widgets.RadioSelect,
        choices=value_as_key([
            'Pro Design - 20/20 .KIT File only',
            'Presentation Pack - 20/20 file plus printable full-color perspective views, floorplan and cabinet elevations, and cabinet quote report (retail).',
            'Not sure.',
        ]),
    )
    revisions = forms.ChoiceField(
        required = False,
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
    tos = forms.BooleanField(widget=forms.CheckboxInput(attrs=attrs_dict),
                             label=_(u'I have read and agree to the Terms of Service'),
                             error_messages={ 'required': _("You must agree to the terms to register") })
    
    def clean_legal_name(self):
        legal_name = self.cleaned_data['legal_name']
        try:
            Dealer.objects.get(legal_name__exact=legal_name)
        except:
            return legal_name
        raise forms.ValidationError(_("A company with that name already exists."))

