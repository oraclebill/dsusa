import os
from decimal import Decimal

from django.conf import settings
from django import forms
import django.db.models as dj_models

from utils.forms import FieldsetForm
from utils.fields import CheckedTextWidget
from product.models import Product

from models import OrderBase, WorkingOrder,  Attachment, Appliance, Moulding


NONE_IMG = settings.MEDIA_URL + 'orders/none.png'

PRO_DESIGN_PROD_ID = 1          ## Yes, very ugly..
PRESENTATION_PACK_PROD_ID = 2



class NewDesignOrderForm(forms.ModelForm):    
    class Meta: 
        model = WorkingOrder
        fields = ['tracking_code', 'project_name', 'project_type', ]
    tracking_code = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    project_type = forms.ChoiceField(choices=OrderBase.Const.PROJECT_TYPE_CHOICES)
    floorplan = forms.FileField(label='Floorplan File', required=False)
    
## TODO: do this right..
def price_order(dealer, product, options={}):
    #TODO: optimize - prices probably don't change very often so prices should be cached..
    product = int(product)
    price = Product.objects.get(pk=product).base_price
    for key, value in options:
        if key =='rush':
            price = price + 20
    return price    

base_product_choices = Product.objects.filter(product_type=Product.Const.BASE).values_list('id', 'name')
#TODO: figure out better programmatic method for finding rush and revision prods.
#revision_product_choices = Product.objects.filter(product_type=Product.Const.OPTION, name__icontains='revision').values_list('id', 'name')
procesing_option_choices = Product.objects.filter(product_type=Product.Const.OPTION, name__icontains='rush').values_list('id', 'name') 
procesing_option_choices.insert(0, ('', ''))
#TODO: support for revisions..

class SubmitForm(forms.ModelForm):
    name = 'Order Submission Info'
                                       
    class Meta:
        model = WorkingOrder
        fields = [
            'tracking_code',
            'project_name',
            'project_type',
            'design_product',
            'client_notes',
        ]

    # widget overrides ...
    tracking_code = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
#    project_type = forms.ChoiceField(widget=forms.Select(attrs={'readonly':'readonly'}))
    
    # will determine 'quoted_cabinet_list, color_views, etc ...
    design_product = forms.ChoiceField(choices=base_product_choices)
    processing_option = forms.ChoiceField(choices=procesing_option_choices)

    def clean(self):
        cleaned_data = self.cleaned_data
        order = self.instance
        #
        if not order.attachments.filter(type__exact=Attachment.FLOORPLAN):
            raise forms.ValidationError('Your order has no attachments! We at least need a flooplan image to continue...')        
        #
        dealer = order.owner.get_profile().account
        try:
            order.cost = price_order(dealer, 
                                     cleaned_data['design_product'], 
                                     options={'rush': cleaned_data['rush']} )
        except Exception, exc_info:
            raise forms.ValidationError('Error: Unable to price order: %s' % exc_info)
        #
        return cleaned_data        

    def save(self, commit=True):
        #
        order = self.instance
        order.rush = bool(self.cleaned_data['processing_option'])
        premium_selected = (self.cleaned_data['design_product'] == PRESENTATION_PACK_PROD_ID)
        order.color_view = order.quoted_cabinet_list  = order.elevations = premium_selected
        return super(SubmitForm, self).save(commit)
             
             
def fieldset_fields(fieldsets):
    fieldlist = []
    for fset in fieldsets:
        fieldlist.extend( fset[1]['fields']) # dups possible..
    return fieldlist


class ManufacturerForm(forms.ModelForm, FieldsetForm):
    DOOR_MATERIALS = (
        'Maple', 'Cherry', 'Alder', 'Lyptus','Birch', 'MDF',
        'Stainless Steel', 'Permafoil' 'Glass'
        )
    FINISHES = ('Stain', 'Paint', 'Natural', 'Glaze')

    class Media:
        css = {'all': ('css/jquery.autocomplete.css',)}
        js = ('js/jquery.autocomplete.js', )
    class Meta:
        model = WorkingOrder
        fieldsets = [
            (None, {
                'fields': ['manufacturer','product_line','cabinet_material', 'door_style', 'finish_type','finish_color','finish_options','drawer_front_style']}),
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
        fieldsets = [
            (None, {
                'fields': ('has_soffits', ),
            }),
            (None, {
                'fields': ('soffit_width', 'soffit_height', 'soffit_depth'),
                'styles': 'toggled-fields',
            }),
        ]
        fields = fieldset_fields(fieldsets)
    fieldsets = Meta.fieldsets
    fieldset_image = NONE_IMG
    clean_has_soffits = _soffit_clean('has_soffits')
    clean_soffit_width = _soffit_clean('soffit_width')
    clean_soffit_height = _soffit_clean('soffit_height')
    clean_soffit_depth = _soffit_clean('soffit_depth')


class DimensionsForm(forms.ModelForm, FieldsetForm):
    name = 'Cabinet Dimensions'
    dimension_style =  forms.ChoiceField(choices=WorkingOrder.STYLE_CHOICES, 
                             widget=forms.RadioSelect(attrs={'class': 'dimension_style'}), 
                             label='Type')
    class Meta:
        model = WorkingOrder
        fieldsets = [
            ('Stacking and Staggering Options', {
                'fields': ['dimension_style'],
                'image': NONE_IMG,
            }),
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
        nargs = kwargs and dict(kwargs, widget=CheckedTextWidget) or {'widget':CheckedTextWidget}
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


        
class AttachmentForm(forms.ModelForm):
    name = 'Client Attachments'
    class Meta:
        model = Attachment
        exclude = ('order','page_count')
    
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

