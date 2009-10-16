"Data and helper for diplaying summary information"
from django.utils.text import capfirst


STEPS_SUMMARY = [
    ('Manufacturer', [
        'cabinet_manufacturer',
        'cabinet_door_style',
        'cabinet_wood',
        'cabinet_finish',
    ]),
    ('Hardware', [
        'door_handle_type',
        'door_handle_model',
        'drawer_handle_type',
        'drawer_handle_model',
    ]),
    ('Moulding', [
    ]),
    ('Soffits', [
        'soffit_width',
        'soffit_height',
        'soffit_depth',
    ]),
    ('Dimensions', [
        'dimension_style',
        'standard_sizes',
        'wall_cabinet_height',
        'vanity_cabinet_height',
        'depth'
    ]),
    ('Corner cabinet', [
        'diagonal_corner_base',
        'diagonal_corner_wall',
        'degree90_corner_base',
        'degree90_corner_wall',
    ]),
    ('Interiors', [
        'lazy_susan',
        'slide_out_trays',
        'waste_bin',
        'wine_rack',
        'plate_rack',
        'apliance_garage'
    ]),
    ('Miscellaneous', [
        'corables',
        'brackets',
        'valance',
        'leas_feet',
        'glass_doors',
        'range_hood',
        'posts',
    ]),
]

SUBMIT_SUMMARY = [
    ('Cabinetary', [
        'cabinet_manufacturer',
        'cabinet_door_style',
        'cabinet_wood',
        'cabinet_finish',
    ]),
    ('Moulding', [
    ]),
    ('Dimensions', [
        'dimension_style',
        'standard_sizes',
        'wall_cabinet_height',
        'vanity_cabinet_height',
        'depth'
    ]),
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
