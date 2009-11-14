"""
Definitions for FieldStone Cabinetry
"""

#
catalog = 'Fieldstone'
#
product_lines = [ 
        'FieldStone',
        'FieldStone Custom',
        # 'FieldStone Custom Inset',
    ]
#
item_types = { 
    'door': [
        'species',
        'stain',
        'glaze',
        'specialty_finish',
        ],
    'drawer': [],
    'handle': [],
    # 'cabinet': [],
    # 'miscellaneous': [],
    }
#
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
doors = list(set(doors_by_species.values()))

species = doors_by_species.keys()

#
# species = [
#         ('Alder', 'Rustic Alder'),
#         ('Cherry', 'Rustic Cherry'),
#         ('Hickory', 'Rustic Hickory'),
#         'Maple',        
#         ('Oak', 'Quarter Sawn Oak'),
#     ]
#
stains_by_species = {
    'maple': [
        'Aegean Mist', 'Black', 'Buttercream', 'Daiquiri', 'Eggnog', 'English Ivy', 'Ivory Cream',
        'Moss Green', 'Macadamia', 'Marshmallow Crm', 'Mushroom', 'Pearl', 'Royal Blue', 'White',
        ],
    'cherry': [
        'brittany', 'burgundy', 'butterscotch', 'capuccino', 'chateaux*', 'chestnut', 'harvest',
        'java', 'meridian', 'natural', 'nutmeg', 'oregano', 'paprika', 'rattan', 'toffee',
        'unfinished',
        ],
    'hickory': [
        'capuccino', 'champagne', 'harvest', 'honey', 'natural', 'nutmeg', 'oregano', 'paprika',
        'toffee', 'unfinished',
         ],    
    'oak': [
        'capuccino', 'champagne', 'harvest', 'honey', 'natural', 'nutmeg', 'oregano', 'paprika',
        'toffee', 'unfinished',
         ],    
    'alder': [
        'brittany', 'burgundy', 'butterscotch', 'capuccino', 'chateaux*', 'chestnut', 'harvest',
        'java', 'meridian', 'natural', 'nutmeg', 'oregano', 'paprika', 'rattan', 'toffee',
        'unfinished',
         ],    
    }
#
stains = list(set(stains_by_species.values()))

glazes_by_species = {
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
glazes = list(set(glazes_by_species.values()))

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
specialty_finish_options_by_species = {
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

# finish characteristics
standard_finish_options_map = {
    'stain': [],  ## std options
    'stain with glaze': ['spattering'], ## std options
    'tinted varnish': (['low sheen'],[]), ## options override - no options
    'tinted varnish with glaze': (['low sheen', 'distressing'], ['no distressing']),## options override
    'cottage':  (['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel'], ['no distressing']),## options override
    }
#
specialty_finish_options_map = {    ## no options by default.. same as a stain for selection purposes
    'amaretto': ['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel', 'rub through on flat surfaces'],
    'bordeaux': ['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel', 'rub through on flat surfaces'],
    'licorice': ['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel'],
    'linen': ['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel'],
    'oatmeal': ['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel'],
    'villa ivory': ['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel'],
    'chateaux': ['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel'],
    'old world distressing': ['low sheen', 'distressing', 'rounded corners', 'worn edges on center panel'],
    }    
#                
finish_characteristics_map = [
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
