from django import forms


class FieldsetForm(object):
    "Base class for forms that have fieldsets"
    fieldsets = None
    field_styles = None
    fieldset_image = None
    
    def get_fieldsets(self):
        return FieldsetList(self, self.fieldsets)


class FieldsetList(object):
    def __init__(self, form, fieldsets):
        self.form = form
        self.fieldsets = fieldsets or [(None, {'fields': form.base_fields.keys()})]
        if not fieldsets and form.fieldset_image is not None:
            self.fieldsets[0][1]['image'] = form.fieldset_image
        
            
    
    def __iter__(self):
        id = 0
        for name, content in self.fieldsets:
            if isinstance(content, (list, tuple)):
                fields = content
                image = None
                styles = None
            else:
                fields = content['fields']
                image = content.get('image')
                styles = content.get('styles')
            yield Fieldset(id, self.form, name, fields, image, styles)
            id += 1


class Fieldset(object):
    def __init__(self, id, form, name, fields, image, styles):
        self.id = id
        self.form = form
        self.name = name
        self.fields = fields
        self.image = image
        self.styles = styles
    
    def __iter__(self):
        for name in self.fields:
            field = self.form[name]
            styles = None
            if self.form.field_styles and name in self.form.field_styles:
                styles = self.form.field_styles[name]
            yield FieldsetField(field, styles)


class FieldsetField(object):
    "Field proxy class that ads is_checkbox attribute"
    
    def __init__(self, field, styles):
        self.field = field
        self.styles = styles
        self.is_checkbox = isinstance(self.field.field.widget, forms.CheckboxInput)
        
    
    def __getattr__(self, attr):
        return getattr(self.field, attr)
    
    def __unicode__(self):
        return unicode(self.field)
