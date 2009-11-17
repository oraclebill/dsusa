from django import template
from django import forms

register = template.Library()


@register.inclusion_tag("wufu/span.html")
def wufu_span(field, classes=''):
    return {'field': field, 'classes': classes}

@register.inclusion_tag("wufu/li.html")
def wufu_li(field, classes='', instructions=''):
    return {'field': field, 'classes': classes, 'instructions': instructions}

@register.filter
def errors_in(form, field_names):
    return any([
        # getattr(form, field).errors for field in field_names.split(',')
        form[field].errors for field in field_names.split(',')
    ])

@register.filter
def is_checkbox(field):
    return isinstance(field.field.widget, forms.CheckboxInput)

