"Data and helper for diplaying summary information"
from django.utils.text import capfirst


MFG_SECTION = ('Cabinet Line Selection', [
        'manufacturer',
        'door_style',
        'drawer_front_style',
        'cabinet_material',
        'finish_type',
        'finish_color',
        'finish_options',
    ])    
    
HARDWARE_SECTION = ('Door/Drawer Hardware Selections', [
        'door_handle_type',
        'door_handle_model',
        'drawer_handle_type',
        'drawer_handle_model',
    ])    
    
MOULDING_SECTION = ('Moulding Selections', [
    ])
    
SOFFIT_SECTION = ('Soffit Dimensions', [
        'has_soffits',
        'soffit_width',
        'soffit_height',
        'soffit_depth',
    ])
    
DIMENSION_SECTION = ('Cabinet Arrangments / Sizing Options', [
        'dimension_style',
        'standard_sizes',
        'wall_cabinet_height',
        'wall_cabinet_depth',
        'base_cabinet_height',
        'base_cabinet_depth',
        'vanity_cabinet_height',
        'vanity_cabinet_depth',
    ])
    
CORNER_CABINET_SECTION = ('Corner Cabinet Options', [
        'diagonal_corner_wall',
        'diagonal_corner_wall_shelv',
        'diagonal_corner_base',
        'diagonal_corner_base_shelv',
        'degree90_corner_wall',
        'degree90_corner_base',
        'degree90_corner_base_shelv',
    ])
    
CABINET_INTERIORS_SECTION = ('Interiors Options', [
        'slide_out_trays',
        'waste_bin',
        'wine_rack',
        'plate_rack',
        'appliance_garage'
    ])
    
MISCELLANEOUS_OPTIONS_SECTION = ('Miscellaneous Options', [
        'corbels',
        'brackets',
        'valance',
        'legs_feet',
        'glass_doors',
        'range_hood',
        'posts',
    ])
            
STEPS_SUMMARY = [
    MFG_SECTION,
    HARDWARE_SECTION,
    MOULDING_SECTION,
    SOFFIT_SECTION,
    DIMENSION_SECTION,
    CORNER_CABINET_SECTION,
    CABINET_INTERIORS_SECTION,
    MISCELLANEOUS_OPTIONS_SECTION,
]

SUBMIT_SUMMARY = [
    MFG_SECTION,
    MOULDING_SECTION,
    DIMENSION_SECTION,
]

def order_summary(order, summary_fields):
    "Return field values from field names and order instance"
    from models import WorkingOrder
    result = []
    for name, list in summary_fields:
        values = []
        for field in list:
            item_name = WorkingOrder._meta.get_field(field).verbose_name
            item_name = capfirst(item_name)
            if hasattr(order, 'get_%s_display' % field):
                item_value = getattr(order, 'get_%s_display' % field)()
            else:
                item_value = getattr(order, field)
            if item_value not in ('', None):
                values.append((item_name,item_value))
        if len(values) > 0:
            result.append((name, values))
    return result
