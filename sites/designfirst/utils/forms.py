from django import forms


class FieldsetForm(object):
    "Base class for forms that have fieldsets"
    
    def get_fieldsets(self):
        return FieldsetList(self, self.fieldsets)


class FieldsetList(object):
    def __init__(self, form, fieldsets):
        self.form = form
        self.fieldsets = fieldsets
    
    def __iter__(self):
        for name, fields in self.fieldsets:
            yield Fieldset(self.form, name, fields)


class Fieldset(object):
    def __init__(self, form, name, fields):
        self.form = form
        self.name = name
        self.fields = fields
    
    def __iter__(self):
        for name in self.fields:
            field = self.form[name]
            yield FieldsetField(field)


class FieldsetField(object):
    "Field proxy class that ads is_checkbox attribute"
    
    def __init__(self, field):
        self.field = field
        self.is_checkbox = isinstance(self.field.field.widget, forms.CheckboxInput)
    
    def __getattr__(self, attr):
        return getattr(self.field, attr)
    
    def __unicode__(self):
        return unicode(self.field)
