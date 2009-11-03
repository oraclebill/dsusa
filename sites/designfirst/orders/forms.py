from django.conf import settings
import os
from decimal import Decimal
from django import forms
import django.db.models as dj_models
from models import WorkingOrder,  Attachment, Appliance, Moulding
from utils.forms import FieldsetForm
from utils.fields import CheckedTextWidget


NONE_IMG = settings.MEDIA_URL + 'orders/none.png'

def fieldset_fields(fieldsets):
    fieldlist = []
    for fset in fieldsets:
        fieldlist.extend( fset[1]['fields']) # dups possible..
    return fieldlist
    
class ManufacturerForm(forms.ModelForm, FieldsetForm):
    class Media:
        css = {'all': ('css/jquery.autocomplete.css',)}
        js = ('js/jquery.autocomplete.js', )
    class Meta:
        model = WorkingOrder
        fieldsets = [
            (None, {
                'fields': ['manufacturer','product_line','cabinet_material','door_style','drawer_front_style','finish_type','finish_color','finish_options']}),
            # ('Notes', {
            #     'fields': ['cabinetry_notes'], 
            #     'styles': 'collapse'}),
        ]
        fields = fieldset_fields(fieldsets)
        
    name = 'Cabinet Line Selection'
    fieldsets = Meta.fieldsets


def HandleType(**kwargs):
    return forms.ChoiceField(choices=WorkingOrder.HANDLE_TYPES, 
                             widget=forms.RadioSelect, 
                             label='Type', **kwargs)

class HardwareForm(forms.ModelForm, FieldsetForm):
    name = 'Hardware Selection'
    door_handle_type = HandleType()
    drawer_handle_type = HandleType()
    class Meta:
        model = WorkingOrder
        fieldsets = [
            ('Door Handle Selection', {
                'fields': ['door_handle_type', 'door_handle_model'], 
                'image':NONE_IMG}),
            ('Drawer Handle Selection', {
                'fields': ['drawer_handle_type', 'drawer_handle_model'], 
                'image':NONE_IMG}),
        ]
        fields = fieldset_fields(fieldsets)
    fieldsets=Meta.fieldsets



class MouldingForm(forms.ModelForm):
    name = 'Moulding Selection'
    class Meta:
        model = Moulding
        fields = ['type', 'name']
    

    
def _soffit_clean(field):
    "if mouldings are selected then soffits are required"
    def wrapper(form):
        value = form.cleaned_data.get(field)
        has_soffits = bool(form.cleaned_data.get('has_soffits'))
        if has_soffits and form.instance.mouldings.all().count() > 0:
            if value in ('', None):
                raise forms.ValidationError('Soffit dimensions must be specified when moldings selected')
        return value
    return wrapper

class SoffitsForm(forms.ModelForm, FieldsetForm):
    name = 'Soffits Information'
    class Meta:
        model = WorkingOrder
        fields = [
            'has_soffits',
            'soffit_width',
            'soffit_height',
            'soffit_depth',
        ]
    fieldset_image = NONE_IMG
    clean_has_soffits = _soffit_clean('has_soffits')
    clean_soffit_width = _soffit_clean('soffit_width')
    clean_soffit_height = _soffit_clean('soffit_height')
    clean_soffit_depth = _soffit_clean('soffit_depth')


class DimensionsForm(forms.ModelForm, FieldsetForm):
    name = 'Cabinet Dimensions'
    dimension_style =  forms.ChoiceField(choices=WorkingOrder.STYLE_CHOICES, 
                             widget=forms.RadioSelect(attrs={'class': 'dimension_style'}), 
                             label='')
    class Meta:
        model = WorkingOrder
        fieldsets = [
            ('Stacking and Staggering Options', {
                'fields': ['dimension_style'] }),
            ('Standard Sizes', {
                'fields': ['standard_sizes'] }),
            ('Wall Cabinets', {
                'fields': ['wall_cabinet_height', 'wall_cabinet_depth']}),
            ('Base Cabinets', {
                'fields': ['base_cabinet_height', 'base_cabinet_depth']}),
            ('Vanity Cabinets', {
                'fields': ['vanity_cabinet_height', 'vanity_cabinet_depth']}),
        ]
        fields = fieldset_fields(fieldsets)
    fieldsets = Meta.fieldsets


class CornerCabinetForm(forms.ModelForm, FieldsetForm):
    name = 'Corner Cabinet Options'
    class Meta:
        model = WorkingOrder
        fieldsets = [
            ('Diagonal corner wall', {
                    'fields': ['diagonal_corner_wall', 'diagonal_corner_wall_shelv'], 
                    'image':NONE_IMG}),
            ('Diagonal corner base', {
                    'fields': ['diagonal_corner_base', 'diagonal_corner_base_shelv'], 
                    'image':NONE_IMG}),
            ('90 Degree corner wall', {
                    'fields': ['degree90_corner_wall'], 
                    'image':NONE_IMG}),
            ('90 Degree corner base', {
                    'fields': ['degree90_corner_base', 'degree90_corner_base_shelv'], 
                    'image':NONE_IMG}),
        ]
        fields = fieldset_fields(fieldsets)
    fieldsets = Meta.fieldsets
    
    field_styles = {
        'diagonal_corner_wall_shelv': 'right_float_field',
        'diagonal_corner_base_shelv': 'right_float_field',
        'degree90_corner_base_shelv': 'right_float_field',
    }
    def __init__(self, *args, **kwargs):
        #Labels/Widget customization
        for name, field in self.base_fields.items():
            field.widget = forms.RadioSelect(choices=field.choices)
            if name.endswith('_shelv'):
                field.label = 'Shelving'
            else:
                field.label = ''
        super(CornerCabinetForm, self).__init__(*args, **kwargs)


class CheckedCharField(forms.CharField):
    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        nargs = kwargs and dict(kwargs, widget=CheckedTextWidget) or {'widget':widget}
        return super(CheckedCharField, self).__init__(max_length, min_length, *args, **nargs)
        
def make_checked_textfield(f):
    if isinstance(f, dj_models.CharField):
        return f.formfield(form_class=CheckedCharField)
    else:
        return f.formfield()

class InteriorsForm(forms.ModelForm, FieldsetForm):
    name = 'Interior Options'
    formfield_callback = make_checked_textfield
    class Meta:
        model = WorkingOrder
        fields = [
            'slide_out_trays',
            'waste_bin',
            'wine_rack',
            'plate_rack',
            'appliance_garage'
        ]
    fieldset_image = NONE_IMG


class MiscellaneousForm(forms.ModelForm, FieldsetForm):
    formfield_callback = make_checked_textfield
    name = 'Miscellaneous Options'
    class Meta:
        model = WorkingOrder
        fields = [
            'corbels',
            'brackets',
            'valance',
            'legs_feet',
            'glass_doors',
            'range_hood',
            'posts',
        ]
    fieldset_image = NONE_IMG


## TODO: do this right..
def price_order(order):
    price = Decimal('85')
    if order.color_views:
        price += 40
        if order.rush:
            price += 50
    else:
        if order.rush:
            price += 40
    return price
    

class SubmitForm(forms.ModelForm):
    name = 'Order Processing Options'
    class Meta:
        model = WorkingOrder
        fields = [
            'project_name',
            'rush',
            'color_views',
            'elevations',
            'quoted_cabinet_list',
            'client_notes',
        ]

    def clean(self):
        cleaned_data = self.cleaned_data
        order = self.instance
        if not order.attachments.filter(type__exact=Attachment.FLOORPLAN):
            raise forms.ValidationError('Valid orders must include at least one floorplan diagram. This one has none.')        
        try:
            order.cost = price_order(order)
        except Exception, exc_info:
            raise forms.ValidationError('Unable to price order. - %s' % exc_info)
        balance = order.owner.get_profile().account.credit_balance
        if balance < order.cost:
            raise forms.ValidationError('Insufficient funds in account - %s' % balance)    
        return cleaned_data        
        
class AttachmentForm(forms.ModelForm):
    name = 'Client Attachments'
    class Meta:
        model = Attachment
        exclude = ('order',)
    
    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file is not None:
            file_name = file.name.lower()
            name, ext = os.path.splitext(file_name)
            if ext not in ('.jpg', '.jpeg', '.png', '.gif', '.pdf'):
                raise forms.ValidationError('"%s" is not allowed file type' % ext)
        return file


class ApplianceForm(forms.ModelForm):
    name = 'Appliances '
    class Meta:
        model = Appliance
        # exclude = ('order',)
