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


class DimensionField(models.CharField):
    def __init__(self, *args, **kwargs):
        super(DimensionField, self).__init__(max_length=100, *args, **kwargs)
    
    def formfield(self, **kwargs):
        defaults = {'max_length': self.max_length,
                    'required': not self.blank}
        defaults.update(kwargs)
        return DimensionFormField(**defaults)
