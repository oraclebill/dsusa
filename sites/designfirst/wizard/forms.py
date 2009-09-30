from django import forms
from models import WorkingOrder


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



class HardwareFrom(forms.ModelForm):
    class Meta:
        model = WorkingOrder
        fields = [
            'door_handle_type',
            'door_handle_model',
            'drawer_handle_type',
            'drawer_handle_model',
        ]