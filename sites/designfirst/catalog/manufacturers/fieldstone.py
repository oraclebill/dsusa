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

doors_by_species = {
    'alder': ['aero', 'aledo*', 'arcata*', 'arden*', 'ashford', 'bainbridge*', 'brighton', 'bristol', 'carlisle*', 'charleston', 'concord*', 'farmington*', 'hampton', 'hanover*', 'harbor*', 'hartford*', 'heritage', 'hudson*', 'madison*', 'manchester', 'milan', 'monroe', 'monte carlo*', 'monterey*', 'portland', 'raleigh', 'shelburne*', 'sheyenne*', 'somerset', 'stratford', 'sycamore*', 'tempe', 'tremont*', 'waldorf', 'winlsow'] , 
    'cherry': ['aero', 'aledo', 'arcata', 'arden*', 'ashford', 'athensi', 'augustine', 'bainbridge*', 'bellmonte', 'breton', 'brighton', 'bristol', 'cannes', 'carlisle', 'carmelo', 'charleston', 'cologne', 'concord', 'fairfieldi', 'farmington', 'glen cove', 'griffith', 'gulfport', 'hampton', 'hanover', 'harbor', 'heritage', 'hudson', 'lacrossei', 'lagrangei', 'lasallei', 'madison*', 'manchester', 'milan', 'monroe', 'monte carlo', 'monterey', 'portland', 'prescott', 'princeton', 'raleigh', 'recina', 'romance', 'seville', 'shelburne*', 'sheyenne', 'somerset', 'stratford', 'sycamore', 'tempe', 'tremont*', 'versailles', 'wakefield', 'waldorf', 'westport', 'winslow', 'woodfield'] , 
    'hickory': ['aero', 'arden*', 'ashford', 'augustine', 'bainbridge*', 'bellmonte', 'breton', 'brighton', 'bristol', 'cannes', 'carlisle', 'carmelo', 'charleston', 'cologne', 'concord', 'farmington', 'griffith', 'hampton', 'hanover', 'harbor', 'heritage', 'hudson', 'madison*', 'manchester', 'milan', 'monroe', 'monte carlo', 'monterey', 'portland', 'prescott', 'princeton', 'raleigh', 'recina', 'romance', 'seville', 'shelburne*', 'somerset', 'stratford', 'tempe', 'tremont*', 'versailles', 'waldorf', 'winslow'] , 
    'maple': ['aero', 'aledo', 'arcata', 'arden', 'ashford', 'athensi', 'augustine', 'bainbridge', 'bellmonte', 'breton', 'brighton', 'bristol', 'cannes', 'carlisle', 'carmelo', 'charleston', 'cologne', 'concord', 'fairfieldi', 'farmington', 'glen cove', 'griffith', 'gulfport', 'hampton', 'hanover', 'harbor', 'heritage', 'hudson', 'lacrossei', 'lagrangei', 'lasallei', 'madison', 'manchester', 'milan', 'monroe', 'monte carlo', 'monterey', 'portland', 'prescott', 'princeton', 'raleigh', 'recina', 'romance', 'seville', 'shelburne', 'sheyenne', 'somerset', 'stratford', 'sycamore', 'tempe', 'tremont', 'versailles', 'wakefield', 'waldorf', 'westport', 'winslow', 'woodfield'] , 
    'newburg': ['ic', 'wh'] , 
    'oak': ['aero', 'arden', 'ashford', 'augustine', 'bainbridge', 'bellmonte', 'breton', 'brighton', 'bristol', 'carlisle', 'carmelo', 'charleston', 'concord', 'farmington', 'griffith', 'hampton', 'hanover', 'harbor', 'heritage', 'hudson', 'madison', 'manchester', 'milan', 'monroe', 'monte carlo', 'monterey', 'portland', 'raleigh', 'recina', 'romance', 'shelburne', 'somerset', 'stratford', 'tempe', 'tremont', 'waldorf', 'winslow'] , 
    'quartersawn oak': ['athensi', 'fairfieldi', 'farmington', 'lacrossei', 'lagrangei', 'lasallei', 'tempe'] , 
    'rst cherry': ['farmington'] , 
    'rst hickory': ['farmington', 'freeport'] , 
    }
    
species_by_door = {
    'aero': ['alder', 'cherry', 'hickory', 'maple', 'oak'] , 
    'aledo': ['cherry', 'maple'] , 
    'aledo*': ['alder'] , 
    'arcata': ['cherry', 'maple'] , 
    'arcata*': ['alder'] , 
    'arden': ['maple', 'oak'] , 
    'arden*': ['alder', 'cherry', 'hickory'] , 
    'ashford': ['alder', 'cherry', 'hickory', 'maple', 'oak'] , 
    'athensi': ['cherry', 'maple', 'qsoak'] , 
    'augustine': ['cherry', 'hickory', 'maple', 'oak'] , 
    'bainbridge': ['maple', 'oak'] , 
    'bainbridge*': ['alder', 'cherry', 'hickory'] , 
    'bellmonte': ['cherry', 'hickory', 'maple', 'oak'] , 
    'breton': ['cherry', 'hickory', 'maple', 'oak'] , 
    'brighton': ['alder', 'cherry', 'hickory', 'maple', 'oak'] , 
    'bristol': ['alder', 'cherry', 'hickory', 'maple', 'oak'] , 
    'cannes': ['cherry', 'hickory', 'maple'] , 
    'carlisle': ['cherry', 'hickory', 'maple', 'oak'] , 
    'carlisle*': ['alder'] , 
    'carmelo': ['cherry', 'hickory', 'maple', 'oak'] , 
    'charleston': ['alder', 'cherry', 'hickory', 'maple', 'oak'] , 
    'cologne': ['cherry', 'hickory', 'maple'] , 
    'concord': ['cherry', 'hickory', 'maple', 'oak'] , 
    'concord*': ['alder'] , 
    'fairfieldi': ['cherry', 'maple', 'qsoak'] , 
    'farmington': ['cherry', 'hickory', 'maple', 'oak', 'qsoak', 'rstcherry', 'rsthickory'] , 
    'farmington*': ['alder'] , 
    'freeport': ['rsthickory'] , 
    'glen cove': ['cherry', 'maple'] , 
    'griffith': ['cherry', 'hickory', 'maple', 'oak'] , 
    'gulfport': ['cherry', 'maple'] , 
    'hampton': ['alder', 'cherry', 'hickory', 'maple', 'oak'] , 
    'hanover': ['cherry', 'hickory', 'maple', 'oak'] , 
    'hanover*': ['alder'] , 
    'harbor': ['cherry', 'hickory', 'maple', 'oak'] , 
    'harbor*': ['alder'] , 
    'hartford*': ['alder'] , 
    'heritage': ['alder', 'cherry', 'hickory', 'maple', 'oak'] , 
    'hudson': ['cherry', 'hickory', 'maple', 'oak'] , 
    'hudson*': ['alder'] , 
    'ic': ['newburg'] , 
    'lacrossei': ['cherry', 'maple', 'qsoak'] , 
    'lagrangei': ['cherry', 'maple', 'qsoak'] , 
    'lasallei': ['cherry', 'maple', 'qsoak'] , 
    'madison': ['maple', 'oak'] , 
    'madison*': ['alder', 'cherry', 'hickory'] , 
    'manchester': ['alder', 'cherry', 'hickory', 'maple', 'oak'] , 
    'milan': ['alder', 'cherry', 'hickory', 'maple', 'oak'] , 
    'monroe': ['alder', 'cherry', 'hickory', 'maple', 'oak'] , 
    'monte carlo': ['cherry', 'hickory', 'maple', 'oak'] , 
    'monte carlo*': ['alder'] , 
    'monterey': ['cherry', 'hickory', 'maple', 'oak'] , 
    'monterey*': ['alder'] , 
    'portland': ['alder', 'cherry', 'hickory', 'maple', 'oak'] , 
    'prescott': ['cherry', 'hickory', 'maple'] , 
    'princeton': ['cherry', 'hickory', 'maple'] , 
    'raleigh': ['alder', 'cherry', 'hickory', 'maple', 'oak'] , 
    'recina': ['cherry', 'hickory', 'maple', 'oak'] , 
    'romance': ['cherry', 'hickory', 'maple', 'oak'] , 
    'seville': ['cherry', 'hickory', 'maple'] , 
    'shelburne': ['maple', 'oak'] , 
    'shelburne*': ['alder', 'cherry', 'hickory'] , 
    'sheyenne': ['cherry', 'maple'] , 
    'sheyenne*': ['alder'] , 
    'somerset': ['alder', 'cherry', 'hickory', 'maple', 'oak'] , 
    'stratford': ['alder', 'cherry', 'hickory', 'maple', 'oak'] , 
    'sycamore': ['cherry', 'maple'] , 
    'sycamore*': ['alder'] , 
    'tempe': ['alder', 'cherry', 'hickory', 'maple', 'oak', 'qsoak'] , 
    'tremont': ['maple', 'oak'] , 
    'tremont*': ['alder', 'cherry', 'hickory'] , 
    'versailles': ['cherry', 'hickory', 'maple'] , 
    'wakefield': ['cherry', 'maple'] , 
    'waldorf': ['alder', 'cherry', 'hickory', 'maple', 'oak'] , 
    'westport': ['cherry', 'maple'] , 
    'wh': ['newburg'] , 
    'winlsow': ['alder'] , 
    'winslow': ['cherry', 'hickory', 'maple', 'oak'] , 
    'woodfield': ['cherry', 'maple'] , 
    }

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

