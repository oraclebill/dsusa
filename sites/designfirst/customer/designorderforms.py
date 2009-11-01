from django import forms
from customer.models import DesignOrder


class DimensionField(forms.CharField):
    """specially formatted to accomodate fractional values well"""
    def __init__(self, required=False, label=None, initial=None, widget=None, help_text=None):
        super(DimensionField, self).__init__(required,label,initial,widget,help_text)
        
    def clean(self, value):
        return value


class BoxDimensionField(forms.CharField):
    """specially formatted to accomodate three (potentially) fractional values (whd) well"""

    def __init__(self, required=False, label=None, initial=None, widget=None, help_text=None):
        super(BoxDimensionField, self).__init__(required,label,initial,widget,help_text)
        
    def clean(self, value):
        return value


class OrderInfo(forms.ModelForm):
    """Information defining the order."""
    
    class Meta:
        model = DesignOrder
        fields = ['project_name', 'description', 'color_views', 'elevations', 'quote_cabinet_list']
        
    name = "Order Info"
    id = 1    
    
class Cabinetry(forms.ModelForm):
    """Cabinet line information."""

    class Meta:
        model = DesignOrder
        fields = ['manufacturer', 'door_style', 'wood', 'stain',
                  'finish_color', 'finish_options', 'cabinetry_notes']

    name = "Cabinetry"
    id = 2    
    
class Hardware(forms.ModelForm):
    """Hardware options"""
    
    class Meta:
        model = DesignOrder
        fields = ['include_hardware', 'door_hardware', 'drawer_hardware']
    
    name = "Hardware"
    id = 3
    
    
class Mouldings(forms.ModelForm):
    """Trim options"""    
    
    class Meta:
        model = DesignOrder
        fields = [ 'ceiling_height', 'crown_mouldings', 'skirt_mouldings', 
                   'soffits', 'soffit_height', 'soffit_width', 'soffit_depth' ]
    
    name = "Mouldings"
    id = 4
    
class CabinetBoxes(forms.ModelForm):
    """docstring for CabinetBoxes"""
    
    class Meta:
        model = DesignOrder
        fields = ['stacked_staggered', 'wall_cabinet_height', 'vanity_cabinet_height', 'vanity_cabinet_depth' ]
    
    name = "Cabinet Boxes"
    id = 5
    
    
class CornerCabinetOptions(forms.ModelForm):
    """docstring for CornerCabinetOptions"""
    
    class Meta:
        model = DesignOrder
        fields = ['corner_cabinet_base_bc', 'corner_cabinet_base_bc_direction', 
                  'corner_cabinet_wall_bc', 'corner_cabinet_wall_bc_direction'] 
    
    name = "Corner Cabinet Options"
    id = 6
    
    
class IslandAndPeninsula(forms.ModelForm):
    ## todo: come back and document 
    
    class Meta:
        model = DesignOrder
        fields = ['island_peninsula_option']
    
    name = "Islands and Peninsulas"
    id = 7
    

class OtherConsiderations(forms.ModelForm):
    ## todo: come back and document 
    
    class Meta:
        model = DesignOrder
        fields = ['countertop_option', 'backsplash', 'toekick']
    
    name = "Other Considerations"
    id = 8
    

class SpaceManagement(forms.ModelForm):
    ## todo: come back and document 
    
    class Meta:
        model = DesignOrder
        fields = [ 'lazy_susan', 'slide_out_trays', 'waste_bin', 'wine_rack', 'plate_rack', 'appliance_garage']
    
    name = "Space Management"
    id = 9
    
    
class Miscellaneous(forms.ModelForm):
    ## todo: come back and document 
    
    class Meta:
        model = DesignOrder
        fields = [ 'corbels_brackets', 'valance', 'waste_bin', 'legs_feet', 'glass_doors', 'range_hood', 'posts' ]
    
    name = "Miscellaneous"
    id = 10
    
    
class Appliances(forms.ModelForm):
    
    class Meta:
        model = DesignOrder
    
    name = "Appliances"
    id = 11
    
    pass

class FloorPlanDiagram(forms.ModelForm):
    
    class Meta:
        model = DesignOrder
        fields = ['client_diagram']
    
    name = "Floor Plan Diagrams"
    fileform = True
    id = 12
    