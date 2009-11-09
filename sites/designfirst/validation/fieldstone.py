product_lines = [ 
        'FieldStone',
        'FieldStone Custom',
        # 'FieldStone Custom Inset',
    ]
#
wood_species = [
        ('Alder', 'Rustic Alder'),
        ('Cherry', 'Rustic Cherry'),
        ('Hickory', 'Rustic Hickory'),
        'Maple',        
        ('Oak', 'Quarter Sawn Oak'),
    ]
#
stains = {
    'maple': [
        'Aegean Mist',
        'Black',
        'Buttercream',
        'Daiquiri',
        'Eggnog',
        'English Ivy',
        'Ivory Cream',
        'Moss Green',
        'Macadamia',
        'Marshmallow Crm',
        'Mushroom',
        'Pearl',
        'Royal Blue',
        'White',
        ],
    'cherry': [
        'brittany',
        'burgundy',
        'butterscotch',
        'capuccino',
        'chateaux*',
        'chestnut',
        'harvest',
        'java',
        'meridian',
        'natural',
        'nutmeg',
        'oregano',
        'paprika',
        'rattan',
        'toffee',
        'unfinished',
        ],
    'hickory': [
        'capuccino',
        'champagne',
        'harvest',
        'honey',
        'natural',
        'nutmeg',
        'oregano',
        'paprika',
        'toffee',
        'unfinished',
         ],    
    'oak': [
        'capuccino',
        'champagne',
        'harvest',
        'honey',
        'natural',
        'nutmeg',
        'oregano',
        'paprika',
        'toffee',
        'unfinished',
         ],    
    'alder': [
        'brittany',
        'burgundy',
        'butterscotch',
        'capuccino',
        'chateaux*',
        'chestnut',
        'harvest',
        'java',
        'meridian',
        'natural',
        'nutmeg',
        'oregano',
        'paprika',
        'rattan',
        'toffee',
        'unfinished',
         ],    
    }
#
glazes = {
    'maple': [
        'bronze',
        'chocolate',
        'latte',
        'vanilla',
        'nickel',
        ],
    'cherry': [
        'chocolate',
        'ebony',
        'capuccino*',
        'toffee*',
        ],
    'hickory': [
        'chocolate',
         ],    
    'oak': [
        'chocolate',
         ],    
    'alder': [
        'chocolate',
        'ebony',
         ]    
    }                
#
standard_finish_options = [
    ('standard sheen', 'low sheen'),
    ('no spattering', 'spattering'),
    ('no distressing','distressing'),
    'rounded corners',
    'worn edges on center panel',
    'rub through on flat surfaces',
    'worm holes',
    'rasping',
    'dips',
    'knife cuts',
    'speckling',
    'padding',
    ]
#
specialty_finish_options = {
    'maple': [
        'Amaretto',
        'Bordeaux',
        'Licorice',
        'Linen',
        'Oatmeal',
        'Villa Ivory',
         ],    
    'cherry': [],    
    'hickory': [
        'licorice',
         ],    
    'oak': [
        '',
         ],    
    'alder': [
        '',
         ],    
    }

##  #############################  ##
##                                 ##
##  #############################  ##

specialty_finish_options = {    ## no options by default.. same as a stain for selection purposes
    'amaretto': ['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel', 'rub through on flat surfaces'],
    'bordeaux': ['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel', 'rub through on flat surfaces'],
    'licorice': ['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel'],
    'linen': ['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel'],
    'oatmeal': ['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel'],
    'villa ivory': ['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel'],
    'chateaux': ['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel'],
    'old world distressing': ['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel'],
    }    
                
# finish characteristics
standard_finish_options = {
    'stain': [],  ## std options
    'stain with glaze': ['spattering'], ## std options
    'tinted varnish': (['low sheen'],[]), ## options override - no options
    'tinted varnish with glaze': (['low sheen', 'distressing'], ['no distressing']),## options override
    'cottage':  (['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel'], ['no distressing']),## options override
    }

finish_characteristics = [
    ('standard sheen', 'low sheen'),
    ('no spattering', 'spattering'),
    ('no distressing','distressing'),
    'rounded corners',
    'worn edges on center panel',
    'rub through on flat surfaces',
    'worm holes',
    'rasping',
    'dips',
    'knife cuts',
    'speckling',
    'padding',
    ]



# lines     
fieldstone_specs = [
    SpecOption('end panel', 
               options={'standard': '1/2" unfinished veneer core plywood', 
                        'finished': 'finished end panels', 
                        'furniture': 'furniture end panels',
                        'flush': 'flush end panels'}),
    SpecOption('tops and bottoms', 
               options={'standard': '1/2" veneer core plywood'}),
    SpecOption('back', 
               options={'standard': '1/4" plywood with veneer exterior'}),
    SpecOption('back rail', 
               options={'standard': '1/2" veneer core plywood'}),
    SpecOption('face frames', 
               options={'standard': '3/4" thick select solid hardwood'}),
    SpecOption('shelves', 
               options={'standard': '3/4" engineered wood surfaced with birch melamine', 
                        'full': 'full depth shelves'}),
    SpecOption('toe boards', 
               options={'standard': '1/2" unfinished veneer core plywood'}), # trim as option?
    SpecOption('interior', 
               options={'standard': 'surfaced with natural birch melamine', 
                        'stained': 'stained', 
                        'full veneer': 'full veneer'}),
    SpecOption('hinges', 
               options={'standard': 'six-way adjustable concealed hinge', 
                        'knife': 'optional on traditional overlay doors only'})
    ]

fieldstone_custom_specs = [
    SpecOption('end panel', 
               options={'standard': '1/2" unfinished veneer core plywood', 
                        'finished': 'finished end panels', 
                        'furniture': 'furniture end panels',
                        'flush': 'flush end panels'}),
    SpecOption('tops and bottoms', 
               options={'standard': '1/2" veneer core plywood'}),
    SpecOption('back', 
               options={'standard': '1/4" plywood with veneer exterior'}),
    SpecOption('back rail', 
               options={'standard': '1/2" thick veneer core plywood'}),
    SpecOption('face frames', 
               options={'standard': '3/4" thick select solid hardwood'}),
    SpecOption('shelves', 
               options={'standard': '3/4" engineered wood surfaced with birch melamine', 
                        'full': 'full depth shelves', 
                        'plywood': 'plywood'}),
    SpecOption('toe boards', 
               options={'standard': 'standard'}), # trim as option?
    SpecOption('interior', 
               options={'standard': 'standard', 
                        'stained': 'stained', 
                        'full veneer': 'full veneer'}),
    SpecOption('hinges', 
               options={'standard': 'six-way adjustable concealed hinge', 
                        'knife': 'optional on traditional overlay doors only'})
    ]        

