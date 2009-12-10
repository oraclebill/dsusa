"Data and helper for diplaying summary information"
from django.utils.text import capfirst
from datetime import datetime

#from models import WorkingOrder

import forms;

TIMETYPE = type(datetime.now())

__forms__ = [    
            forms.ManufacturerForm,
            forms.HardwareForm,
            forms.MouldingForm,
            forms.SoffitsForm,
            forms.DimensionsForm,
            forms.CornerCabinetForm,
            forms.InteriorsForm,
            forms.MiscellaneousForm,
            forms.AttachmentForm,
            forms.ApplianceForm,
            forms.SubmitForm,
        ]

def make_summary(form):
    name = form.name
    fset_list = getattr(form, 'fieldsets', None)
    if not fset_list:
        fset_list = [(None, {'fields': form.base_fields.keys()})]
    return (name, forms.fieldset_fields(fset_list))
        
MFG_SECTION, HARDWARE_SECTION, MOULDING_SECTION, SOFFIT_SECTION, DIMENSION_SECTION, CORNER_CABINET_SECTION, CABINET_INTERIORS_SECTION, MISCELLANEOUS_OPTIONS_SECTION, ATTACHMENT_SECTION, APPLIANCE_SECTION, TRACKING_SECTION = [ make_summary(f) for f in __forms__ ]
            
STEPS_SUMMARY = [
    MFG_SECTION,
    HARDWARE_SECTION,
    SOFFIT_SECTION,
    DIMENSION_SECTION,
    CORNER_CABINET_SECTION,
    CABINET_INTERIORS_SECTION,
    MISCELLANEOUS_OPTIONS_SECTION,
]

SUBMIT_SUMMARY = [
    MFG_SECTION,
    DIMENSION_SECTION,
]

def order_summary(order, summary_fields):
    "Return field values from field names and order instance"
    from models import WorkingOrder
    result = []
    for name, list in summary_fields:
        values = []
        for val in list:
            if hasattr(val, '__iter__'):
                field, val = val
            else:
                field = val
            item_name = WorkingOrder._meta.get_field(field).verbose_name
            item_name = capfirst(item_name)
            if hasattr(order, 'get_%s_display' % field):
                item_value = getattr(order, 'get_%s_display' % field)()
            else:
                item_value = getattr(order, field)
            if type(item_value) == type(True):
                item_value = item_value and 'Yes' or 'No'
            elif type(item_value) == type(TIMETYPE):
                item_value = item_value.date().isoformat()
            if item_value not in ('', None):
                values.append((item_name,item_value))
        if len(values) > 0:
            result.append((name, values))
    return result
