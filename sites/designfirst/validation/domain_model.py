class Catalog(object):
    pass

class CatalogItem(object):
    __slots__ = ['catalog',         ## which catalog i belong to  
                 'item_code',       ## a.k.a. nomenclature ?
                 'upcharge',        ## if I have one, what is it 
                 'extended_lead_time',       ## e.g. 'special order?'
                 ]

class Specification(object):
    __slots__ = ['spec_areas']          ## a collection of SpecificationAreas
    
class SpecificationDomain(object):
    __slots__ = ['domain',              ## e.g. 'end panels' 
                 'description',         ## 
                 'type',                ## e.g. option-list 
                 'selectable_options',  ## default-value == options[0]
                ]
    
class SpecOption(object):
    __slots__ = ['nomenclature', 'name', 'description', 'benefits', 'pricing_impact', 
                 'requires', 'restricts', 'replaces', 'recommends', ]
    
    def __init__(self, name, description=None, nomenclature=None, options=None ):
        self.name = name
        self.description = description
        self.nomenclature = nomenclature
        self.options = options

class WoodSpecies(object):
    __slots__ = ['name', 'description', 'lines', 'door_styles', 'notes', 'cautions', 'pricing_impact']
    
class Stain(object):
    __slots__ = ['name', 'description', 'eligible_lines', 'eligible_species', 'standard_characteristics', 'finish_options', 
                 'palette', 'door_styles', 'upcharges']

class Glaze(object):
    __slots__ = ['name', 'description', 'lines', 'door_styles', 'notes', 'cautions', 'pricing_impact']

class FinishOption(object):  ## catalog: styling options
    __slots__ = ['line', 'species', 'palette', 'door_styles', 'upcharge' ]


