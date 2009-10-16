import os
from django import forms
from models import WorkingOrder,  Attachment, Appliance, Moulding
from utils.forms import FieldsetForm


class MockForm(forms.ModelForm):
    class Meta:
        model = WorkingOrder
        fields = [
            'cabinetry_notes'
        ]




class ManufacturerForm(forms.ModelForm):
    class Meta:
        model = WorkingOrder
        fields = [
            'cabinet_manufacturer',
            'cabinet_product_line',
            'cabinet_door_style',
            'cabinet_wood',
            'cabinet_finish',
            'cabinet_finish_options',
            'cabinetry_notes'
        ]
    
    class Media:
        css = {'all': ('css/jquery.autocomplete.css',)}
        js = ('js/jquery.autocomplete.js', )



def HandleType(**kwargs):
    return forms.ChoiceField(choices=WorkingOrder.HANDLE_TYPES, 
                             widget=forms.RadioSelect, 
                             label='Type', **kwargs)

class HardwareForm(forms.ModelForm, FieldsetForm):
    door_handle_type = HandleType()
    drawer_handle_type = HandleType()
    class Meta:
        model = WorkingOrder
        fields = [
            'door_handle_type',
            'door_handle_model',
            'drawer_handle_type',
            'drawer_handle_model',
        ]
    fieldsets = [
        ('Door', ['door_handle_type', 'door_handle_model']),
        ('Drawer', ['drawer_handle_type', 'drawer_handle_model']),
    ]




class MouldingForm(forms.ModelForm):
    class Meta:
        model = Moulding
        fields = ['type', 'name']
    

    
def _soffit_clean(field):
    "if mouldings are selected then soffits are required"
    def wrapper(form):
        value = form.cleaned_data.get(field)
        if form.instance.mouldings.all().count() > 0:
            if value in ('', None):
                raise forms.ValidationError('This field is required')
        return value
    return wrapper

class SoffitsForm(forms.ModelForm):
    class Meta:
        model = WorkingOrder
        fields = [
            'soffit_width',
            'soffit_height',
            'soffit_depth',
        ]
    clean_soffit_width = _soffit_clean('soffit_width')
    clean_soffit_height = _soffit_clean('soffit_height')
    clean_soffit_depth = _soffit_clean('soffit_depth')


class DimensionsForm(forms.ModelForm, FieldsetForm):
    dimension_style =  forms.ChoiceField(choices=WorkingOrder.STYLE_CHOICES, 
                             widget=forms.RadioSelect(attrs={'class': 'dimension_style'}), 
                             label='')
    class Meta:
        model = WorkingOrder
        fields = [
            'dimension_style',
            'standard_sizes',
            'wall_cabinet_height',
            'vanity_cabinet_height',
            'depth'
        ]
    fieldsets = [
        ('Stacking and Staggering Options', ['dimension_style']),
        ('Sizes', ['standard_sizes', 'wall_cabinet_height', 'vanity_cabinet_height', 'depth']),
    ]


class CornerCabinetForm(forms.ModelForm, FieldsetForm):
    class Meta:
        model = WorkingOrder
        fields = [
            'diagonal_corner_base',
            'diagonal_corner_base_shelv',
            'diagonal_corner_wall',
            'diagonal_corner_wall_shelv',
            'degree90_corner_base',
            'degree90_corner_base_shelv',
            'degree90_corner_wall',
        ]
    fieldsets = [
        ('Diagonal corner wall', ['diagonal_corner_wall', 'diagonal_corner_wall_shelv']),
        ('Diagonal corner base', ['diagonal_corner_base', 'diagonal_corner_base_shelv']),
        ('90 Degree corner wall', ['degree90_corner_wall']),
        ('90 Degree corner base', ['degree90_corner_base', 'degree90_corner_base_shelv']),
    ]
    def __init__(self, *args, **kwargs):
        #Labels/Widget customization
        for name, field in self.base_fields.items():
            field.widget = forms.RadioSelect(choices=field.choices)
            if name.endswith('_shelv'):
                field.label = 'Shelving'
            else:
                field.label = ''
        super(CornerCabinetForm, self).__init__(*args, **kwargs)


class InteriorsForm(forms.ModelForm, FieldsetForm):
    class Meta:
        model = WorkingOrder
        fields = [
            'lazy_susan',
            'slide_out_trays',
            'waste_bin',
            'wine_rack',
            'plate_rack',
            'apliance_garage'
        ]


class MiscellaneousForm(forms.ModelForm, FieldsetForm):
    class Meta:
        model = WorkingOrder
        fields = [
            'corables',
            'brackets',
            'valance',
            'leas_feet',
            'glass_doors',
            'range_hood',
            'posts',
        ]


class SubmitForm(forms.ModelForm):
    class Meta:
        model = WorkingOrder
        fields = [
            'color_views',
            'elevations',
            'quoted_cabinet_list',
        ]


class AttachmentForm(forms.ModelForm):
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
    class Meta:
        model = Appliance
        exclude = ('order',)
