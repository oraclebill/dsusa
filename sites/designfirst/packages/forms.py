from django import forms

class NewPackageForm(forms.Form):
    
    orderid         = forms.IntegerField()
    package_type    = forms.ChoiceField(choices=(('STANDARD', 'Standard'), 
                                                 ('CORRECTION', 'Correction'), 
                                                 ('UPDATE', 'Update')))
    related_packageid = forms.ChoiceField()
    designer        = forms.CharField()
    created_by      = forms.CharField()         # session user
    created_on      = forms.DateTimeField()     # current date
    notes           = forms.CharField(widget=forms.Textarea) 
    frozen          = forms.BooleanField()
    
    def __init__(self, choices=None, **kwargs):
        super(NewPackageForm, self).__init__(**kwargs)
        if choices:
            self.fields['related_packageid'].choices = [(id,id) for id in choices]            
        
           
