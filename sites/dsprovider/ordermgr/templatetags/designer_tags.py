from django import template

register = template.Library()

class RowIf(template.Node):
    
    def __init__(self,model,field,default,selector):
        self._modelobj = template.Variable(model)
        self._field = field
        self._default = default
        self._selector = selector
    
    def render(self,context):        
        if self._selector:
            field_obj = template.Variable(self._field).resolve(context)
        else:
            field_obj = self._modelobj.resolve(context)._meta.get_field(self._field)
        model_obj = self._modelobj.resolve(context)
        field_val = field_obj.value_from_object(model_obj)
        if not field_val:
            field_val = self._default
        if not field_val:
            return ''
        else:            
            ctx = template.Context({
                'name':field_obj.verbose_name,
                'type':field_obj.db_type(),
                'value':field_val,
                'meta': vars(field_obj)
                })
            t = template.loader.get_template('designer/tags/row_if.html')
            return t.render(ctx)
        
def parse_row_if(parser,token):
    """
    Process a 'row_if' node. 
    
    Of the form: 
        {% row_if model.field [default] %} 
            where <model> is a model instance and <field> is an attribute, or
        {% row_if model:field [default] %}  
            where <model> is a model instance, and <field> is a django.models.Field object.
    """
        
    try:
        bits = token.split_contents()[1:]
        model_and_field = bits.pop(0)
    except Exception, e:
        raise template.TemplateSyntaxError, 'Invalid temple node: %s' % token.split_contents()[0]
        
    if bits:
        default = bits.pop(0)
        if default[0] in '"''' and default[-1] in '"''' and default[0] == default[-1] and len(default) > 1:
            default = default[1:-1]
    else:
        default = None
        
    if bits:
        raise template.TemplateSyntaxError, '%s: too many arguments' % token.split_contents()[0]
        
    selector = False
    try:
        if ':' in model_and_field:
            selector = True
            model,field = model_and_field.split(':')
        else:
            model,field = model_and_field.split('.')
    except:
        raise template.TemplateSyntaxError, '%s: first parameter must be of form <model>[.:]<field>, got "%s"' % (token.split_contents()[0], model_and_field)
    
    return RowIf(model,field,default,selector)
    
register.tag('row_if', parse_row_if)