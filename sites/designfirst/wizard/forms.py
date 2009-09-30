from django import forms
from models import WorkingOrder
from utils.forms import FieldsetForm


class MockForm(forms.ModelForm):
    class Meta:
        model = WorkingOrder
        fields = [
            'cabinetry_notes'
        ]




class ManufacturerFrom(forms.ModelForm):
    class Meta:
        model = WorkingOrder
        fields = [
            'cabinet_manufacturer',
            'cabinet_door_style',
            'cabinet_wood',
            'cabinet_finish',
            'cabinetry_notes'
        ]
    
    class Media:
        css = {'all': ('css/jquery.autocomplete.css',)}
        js = ('js/jquery.autocomplete.js', )



def HandleType(**kwargs):
    return forms.ChoiceField(choices=WorkingOrder.HANDLE_TYPES, 
                             widget=forms.RadioSelect, 
                             label='Type', **kwargs)

class HardwareFrom(forms.ModelForm, FieldsetForm):
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




class MouldingFrom(forms.ModelForm, FieldsetForm):
    class Meta:
        model = WorkingOrder
        fields = [
            'celiling_height',
            'crown_moulding_type',
            'skirt_moulding_type',
            'soft_width',
            'soft_height',
            'soft_depth',
        ]
    fieldsets = [
        (None, ['celiling_height', 'crown_moulding_type', 'skirt_moulding_type']),
        ('Soft', ['soft_width', 'soft_height', 'soft_depth']),
    ]


class DimensionsForm(forms.ModelForm, FieldsetForm):
    dimension_style =  forms.ChoiceField(choices=WorkingOrder.STYLE_CHOICES, 
                             widget=forms.RadioSelect, label='')
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
        ('Style', ['dimension_style']),
        ('Sizes', ['standard_sizes', 'wall_cabinet_height', 'vanity_cabinet_height', 'depth']),
    ]
