# -*- coding: utf-8 -*-
from django.utils.safestring import mark_safe
import re
from django.db import models
from django import forms

dimension_re = re.compile(r'\d+[\d\\/\'"\s"’`]*')

TEST_DATA = ('12', '12"', '10’', "12'", '12"', '42’ 3 1/2"')

for s in TEST_DATA:
    assert dimension_re.match(s), '"%s" does not match re-pattern' % s
    
VALID_EXAMPLES = ('12', '12"', '10’', '42’ 3 1/2"')


class DimensionFormField(forms.RegexField):
    default_error_messages = {
        'invalid': mark_safe('Invalid value format. Valid Examples:<br> %s' % '<br>'.join(VALID_EXAMPLES))
    }

    def __init__(self, max_length=None, min_length=None, *args, **kwargs):
        forms.RegexField.__init__(self, dimension_re, max_length, min_length, *args,
                            **kwargs)


class CheckedTextWidget(forms.widgets.MultiWidget):
    class Media:
        css = {
            'all': ('checkedtext.css',)
        }
        js = ('js/jquery-1.3.2.min.js', 'js/checkedtext.js')
        
    def __init__(self, attrs=None):
        widgets = [forms.fields.CheckboxInput, forms.fields.TextInput]
        super(CheckedTextWidget, self).__init__(widgets, attrs)
        
    def decompress(self, value):
        if value:
            return (True, value)
        return (False, value)
        
    def render(self, name, value, attrs=None):
        # value is a list of values, each corresponding to a widget
        # in self.widgets.
        if not isinstance(value, list):
            value = self.decompress(value)
        output = []
        final_attrs = self.build_attrs(attrs)
        id_ = final_attrs.get('id', None)
        cl = final_attrs.get('class', '')
        cl += ' cktxt'        
        final_attrs['class']=cl
        checkbox = self.widgets[0]
        if id_:
            final_attrs = dict(final_attrs, id='%s_ck' % id_)
        output.append(checkbox.render(name + '_ck', value[0], final_attrs))
        charfield = self.widgets[1]
        if id_:
            final_attrs = dict(final_attrs, id='%s' % id_)
        if not value[0]:
            final_attrs = dict(final_attrs,  style='display: none;')
        output.append(charfield.render(name + '_txt', value[1], final_attrs))
        return mark_safe(self.format_output(output))
        

class DimensionField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(DimensionField, self).__init__(max_length=100, *args, **kwargs)
    
    def formfield(self, **kwargs):
        defaults = {'max_length': self.max_length,
                    'required': not self.blank}
        defaults.update(kwargs)
        return DimensionFormField(**defaults)
