"""
Definitions for FieldStone Cabinetry

    cabinet line intializers - 
        self.door_info = module.door_info
        self.primary_finish_types = module.primary_finish_types
        self.finish_option_types = module.finish_option_types
        self.special_finish_options = module.special_finish_options
        self.finish_options = module.finish_options

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
#item_types = { 
#    'door': [
#        'species',
#        'stain',
#        'glaze',
#        'specialty_finish',
#        ],
#    'drawer': [],
#    'handle': [],
#    # 'cabinet': [],
#    # 'miscellaneous': [],
#    }
#


_oak_stains = ['Capuccino', 'Champagne', 'Harvest', 'Honey', 'Natural', 'Nutmeg', 'Oregano', 'Paprika', 'Toffee', 'Unfinished']
_cherry_stains = ['Brittany', 'Burgundy', 'Butterscotch', 'Capuccino', 'Chateaux', 'Chestnut', 'Harvest', 'Java', 'Meridian', 'Natural', 'Nutmeg', 'Oregano', 'Paprika', 'Rattan', 'Toffee', 'Unfinished']
_hickory_stains = ['Capuccino', 'Champagne', 'Harvest', 'Honey', 'Natural', 'Nutmeg', 'Oregano', 'Paprika', 'Toffee', 'Unfinished']
#
_alder_cherry_old_world_stains = ['Brittany Chocolate', 'Butterscotch Chocolate', 'Cappuccino Chocolate', 'Harvest Chocolate', 'Natural Chocolate', 'Nutmeg Chocolate', 'Oregano Chocolate']
_maple_old_world_stains = ['Amber Chocolate', 'Butterscotch Chocolate', 'Cappuccino Chocolate', 'Caramel Chocolate', 'Champagne Chocolate', 'Daiquiri Chocolate', 'Honey Chocolate', 'Macadamia Chocolate', 'Marshmallow Crm Chocolate', 'Natural Chocolate', 'Oregano Chocolate',  'Paprika Chocolate']
_specialty_old_world_stains = ['Amaretto', 'Bordeaux', 'Linen Ivory', 'Linen Mushroom', 'Linen White',]
# 
_cherry_glazes  = ['Chocolate','Ebony','Capuccino','Toffee']
_hickory_glazes = ['Chocolate',]
_special_finish_options = ['Amaretto', 'Bordeaux', 'Licorice', 'Linen', 'Oatmeal', 'Villa Ivory']

finish_options = ['Low Sheen', 'Spattering', 'Distressing', 'Rounded Corners', 'Worn Edges On Center Panel', 'Rub Through On Flat Surfaces', 'Worm Holes', 'Rasping', 'Dips', 'Knife Cuts', 'Speckling', 'Padding']

primary_finish_types = ['stain', 'tinted varnish', 'old world distressed']
finish_option_types = ['glaze', 'standard finish option', 'special finish option', 'old world specialty option']
door_info = {
    'alder': { 
        'style': ['Aero', 'Aledo', 'Arcata', 'Arden', 'Ashford', 'Bainbridge', 'Brighton', 'Bristol', 'Carlisle', 'Charleston', 'Concord', 'Farmington', 'Hampton', 'Hanover', 'Harbor', 'Hartford', 'Heritage', 'Hudson', 'Madison', 'Manchester', 'Milan', 'Monroe', 'Monte Carlo', 'Monterey', 'Portland', 'Raleigh', 'Shelburne', 'Sheyenne', 'Somerset', 'Stratford', 'Sycamore', 'Tempe', 'Tremont', 'Waldorf', 'Winlsow'] ,
        'stain': _cherry_stains,
        'old world distressed': _alder_cherry_old_world_stains,
        'glaze': ['chocolate', 'ebony'],
        'standard finish option':  finish_options,
        'special finish option':  [],
    },
    'cherry': { 
        'style': ['Gulfport', 'Bristol', 'Farmington', 'Hudson', 'Monroe', 'Athens', 'Romance', 'Shelburne', 'Ashford', 'Bainbridge', 'Heritage', 'Westport', 'Somerset', 'Seville', 'Winslow', 'Versailles', 'Monte Carlo', 'Glen Cove', 'Arden', 'Aero', 'Wakefield', 'Recina', 'Lacrosse', 'Stratford', 'Brighton', 'Hanover', 'Princeton', 'Harbor', 'Woodfield', 'Sycamore', 'Madison', 'Bellmonte', 'Waldorf', 'Arcata', 'Raleigh', 'Cannes', 'Tremont', 'Prescott', 'Charleston', 'Lagrange', 'Carmelo', 'Monterey', 'Hampton', 'Sheyenne', 'Augustine', 'Concord', 'Lasalle', 'Cologne', 'Fairfield', 'Milan', 'Manchester', 'Aledo', 'Tempe', 'Portland', 'Griffith', 'Breton', 'Carlisle'].sort() ,
        'stain': _cherry_stains, 
        'glaze': _cherry_glazes, 
        'old world distressed': _alder_cherry_old_world_stains,
        'standard finish option':  finish_options,
        'special finish option':  [],
    },
    'hickory': { 
        'style': ['Cannes', 'Farmington', 'Hudson', 'Romance', 'Shelburne', 'Ashford', 'Bainbridge', 'Heritage', 'Somerset', 'Winslow', 'Versailles', 'Monte Carlo', 'Arden', 'Aero', 'Recina', 'Stratford', 'Brighton', 'Hanover', 'Princeton', 'Harbor', 'Madison', 'Bellmonte', 'Waldorf', 'Raleigh', 'Bristol', 'Tremont', 'Prescott', 'Charleston', 'Carmelo', 'Monterey', 'Hampton', 'Tempe', 'Augustine', 'Concord', 'Seville', 'Cologne', 'Milan', 'Manchester', 'Monroe', 'Portland', 'Griffith', 'Breton', 'Carlisle'] ,
        'stain': _hickory_stains, 
        'glaze': _hickory_glazes, 
        'standard finish option':  finish_options,
        'special finish option':  ['Licorice'],
    },
    'maple': { 
        'style': ['Aero', 'Bristol', 'Farmington', 'Hudson', 'Monroe', 'Athens', 'Romance', 'Gulfport', 'Ashford', 'Heritage', 'Westport', 'Somerset', 'Seville', 'Winslow', 'Versailles', 'Monte Carlo', 'Glen Cove', 'Tempe', 'Arden', 'Wakefield', 'Recina', 'Lacrosse', 'Stratford', 'Shelburne', 'Brighton', 'Hanover', 'Princeton', 'Harbor', 'Woodfield', 'Sycamore', 'Madison', 'Bellmonte', 'Waldorf', 'Arcata', 'Raleigh', 'Cannes', 'Prescott', 'Charleston', 'Tremont', 'Lagrange', 'Carmelo', 'Monterey', 'Hampton', 'Sheyenne', 'Augustine', 'Concord', 'Lasalle', 'Cologne', 'Fairfield', 'Milan', 'Manchester', 'Aledo', 'Bainbridge', 'Portland', 'Griffith', 'Breton', 'Carlisle'],
        'stain': ['Amber', 'Butterscotch', 'Capuccino', 'Caramel', 'Champagne', 'Chestut', 'Honey', 'Natural', 'Oregano', 'Paprika', 'Unfinished'],
        'tinted varnish': ['Aegean Mist', 'Black', 'Buttercream', 'Daiquiri', 'Eggnog', 'English Ivy', 'Ivory Cream', 'Moss Green', 'Macadamia', 'Marshmallow Crm', 'Mushroom', 'Pearl', 'Royal Blue', 'White'],
        'old world distressed': _maple_old_world_stains,
        'old world specialty option': _specialty_old_world_stains,
        'glaze': ['Bronze', 'Chocolate', 'Latte', 'Vanilla', 'Nickel'], 
        'standard finish option':  finish_options,
        'special finish option':  ['Amaretto','Bordeaux','Licorice','Linen','Oatmeal','Villa Ivory'],
    },
    'rigid thermo foil': { 
        'style': ['Newburg',] , 
        'tinted varnish': ['Ivory Cream', 'White'],
    },
    'oak': { 
        'style': ['Aero', 'Monte Carlo', 'Farmington', 'Hudson', 'Romance', 'Ashford', 'Heritage', 'Somerset', 'Winslow', 'Shelburne', 'Tempe', 'Arden', 'Recina', 'Stratford', 'Brighton', 'Hanover', 'Harbor', 'Madison', 'Bellmonte', 'Waldorf', 'Raleigh', 'Bristol', 'Charleston', 'Tremont', 'Carmelo', 'Monterey', 'Hampton', 'Augustine', 'Concord', 'Milan', 'Manchester', 'Monroe', 'Bainbridge', 'Portland', 'Griffith', 'Breton', 'Carlisle'] ,
        'stain': _oak_stains, 
        'glaze': _hickory_glazes, 
        'standard finish option':  finish_options,
        'special finish option':  [],
    },
    'quartersawn oak': { 
        'style': ['Athens', 'Fairfield', 'Farmington', 'Lacrosse', 'Lagrange', 'Lasalle', 'Tempe'] , 
        'stain': _oak_stains, 
        'glaze': _hickory_glazes, 
        'standard finish option':  finish_options,
        'special finish option':  [],
    },
    'rustic cherry': { 
        'style': ['Farmington'] , 
        'stain': _cherry_stains, 
        'glaze': _cherry_glazes, 
        'standard finish option':  finish_options,
        'special finish option':  [],
    },
    'rustic hickory': { 
        'style': ['Farmington', 'Freeport'] , 
        'stain': _hickory_stains, 
        'glaze': _hickory_glazes, 
        'standard finish option':  finish_options,
        'special finish option':  [],
    },
}

# finish characteristics -- fieldstone specific..
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

