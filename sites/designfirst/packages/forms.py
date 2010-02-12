from django import forms

class NewPackageForm(forms.Form):
    
    orderid         = forms.IntegerField(label="Order ID")
    package_type    = forms.ChoiceField(label="Package Type",
                                        choices=(('STANDARD', 'Standard'), 
                                                 ('CORRECTION', 'Correction'), 
                                                 ('UPDATE', 'Update')))
    related_packageid = forms.ChoiceField(label="Related Package ID",
                                          help_text="For update or corrections orders, this field identifies the package being modified")
    designer        = forms.CharField(label="Designer")
#    created_by      = forms.CharField(label="Creator")         # session user
#    created_on      = forms.DateTimeField(label="Created")     # current date
    notes           = forms.CharField(widget=forms.Textarea) 
    frozen          = forms.BooleanField()
    
    def __init__(self, orderid=None, choices=None, **kwargs):
        super(NewPackageForm, self).__init__(**kwargs)
        if orderid:
            field = self.fields['orderid']
            field.initial = orderid
            widget = field.widget
            widget.attrs = { 'readonly': 'readonly' } 
        if choices:            
            self.fields['related_packageid'].choices = [(id,id) for id in choices]
        else:
            self.fields['related_packageid'].widget.attrs = { 'disabled': 'disabled' }
                        
        
class PackageFilesForm(forms.Form):
    
    kitfile = forms.FileField()
    quotefile = forms.FileField()