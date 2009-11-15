

def _get_options_for_attribute(attr, species=None, style=None, line=None):
    """ 
    for each attribute in the master map (door_info), returns the union of all options for that attribute.
    
    >>> door_info = { 'test': { 'first': [1, 2, 3], 'second': [ 'x' ] }, 'test2': { 'first': [100,200,300], 'second': [ 'ecks' ] } }
    >>> set(_all_materials('first')) == set([1, 2, 3, 100, 200, 300]) 
    >>> set(_all_materials('second')) == set(['x', 'ecks']) 
    """
    return species and door_info[species][attr] or \
        list(set(reduce(list.__add__, [d[attr] for d in door_info.values()]))) 
        
def get_product_lines():
    return product_lines

def get_door_materials(style=None, line=None):
    if style:
        return [key for key in door_info.keys() if style in door_info[key]['style']]
    else:
        return door_info.keys()

def get_primary_finish_types(species=None, style=None, line=None):
    if style:
        raise NotImplementedError('style query not supported')
    if species: 
        return [key for key in door_info[species].keys() if key in primary_finish_types]
    else: 
        return primary_finish_types[:]

def get_finish_option_types(species=None, finish_type=None, style=None, line=None):
    if style:
        raise NotImplementedError('style query not supported')
    if species: 
        return [key for key in door_info[species].keys() if key in finish_options]
    else: 
        return finish_options[:]

def get_door_styles(species=None, line=None ):
    return _get_options_for_attribute('style', species)
    
def get_primary_finishes(finish_type=None, species=None, style=None, line=None):
    return finish_type and _get_options_for_attribute(finish_type, species) or \
            set(reduce(list.__add__, [_get_options_for_attribute(key, species) for key in primary_finish_types]))
    
def get_finish_options(option_type=None, species=None, style=None, line=None):
    return option_type and _get_options_for_attribute(option_type, species) or \
            set(reduce(list.__add__, [_get_options_for_attribute(key, species) for key in finish_options]))

    
product_lines = [ 
        'Executive',
        'Bellini',
        'Biltmore',
#        'impact'  # no data...
    ]    
#
primary_finish_types = ['paint', 'stain']
finish_options = ['glaze', 'standard finish option', 'special finish option']

std_door_styles = [
        'bali', 'bel air', 'bitlmore estate', 'bitlmore manor', 'bitlmore vineyard', 'boca',
        'bombay', 'brittany', 'broadway', 'camelot', 'camelot beaded', 'charleston', 'charleston reversed', 
        'contemporary slab', 'cumberland', 'georgetown', 'harvest', 'harvest reversed',
        'hilton', 'huntington', 'lattice', 'louvre solid', 'louvre vented', 'midtown', 'normandy',
        'plaza', 'quinta', 'rockefeller', 'romanesque', 'saratoga', 'shaker 1/4 beaded', 'shaker 3',
        'shaker 3 reversed', 'shaker 4', 'shaker double', 'shaker single', 'shaker solid beaded',
        'tiffany', 'traditional', 'traditional beaded', 'traditional reversed', 'tuscany', 'villa',
        'williamsburg', 'wood veneer', 
    ]
thermafoil_or_metal_styles = [ 
        'allegro', 'alpha', 'beta',
        'chateau', 'classic shaker', 'cosmos', 'dakota', 'designer', 'euro', 'gamma', 'glamour',
        'loft', 'milano', 'new yorker', 'omega', 'revere', 'sahara', 'shaker beaded', 'slab mdf',
        'tempo', 'traditional shaker', 'ultra', 'vogue foil', 'zephyr',
    ]
finish_options = [
    'flyspeck', 'grain cracking', 'heavy rustic distressing', 'lite weathered distressing', 
    'low sheen' 'random scraped edges', 'rub thru', 'spot crackle', 'wormhole',
]
#
special_finish_options = [
    'biltmore finishes', 'brushed glaze', 'island finish',
]
#   

door_info = {
    'maple': { 
        'stain': [
    		'Amaretto', 'Autumn', 'Barley', 'Black', 'Blue Wash', 'Burgundy', 'Caramel', 'Cinnamon',
            'Cream', 'Desert Mist', 'Fruitwood', 'Green Wash', 'Hazelnut Ivory', 'Honey', 'Island',
            'Lemon', 'London Fog', 'Natural Maple', 'Nutmeg', 'Pearl', 'Pecan', 'Raisin', 
            'Red Wash', 'Vanilla', 'Walnut', 'Wheat', 'Wild Honey',
            ],
        'glaze': [
            'chocolate', 'coffee', 'linen', 'pewter', 'sueded', 'tan', 'white'
            ],
        'style': std_door_styles,
        'standard finish option':  finish_options,
        'special finish option':  special_finish_options,
    },
    'cherry': { 
        'stain' : [
            'natural cherry', 'cherry cafe', 'cherry merlot', 'cherry spice', 'cherry espresso',
            'cherry mocha', 'cherry moroccan', 'cherry port',
            ],
        'glaze': [
            'chocolate', 'coffee', 'linen', 'pewter', 'sueded', 'tan', 'white'
            ],
        'style': std_door_styles,
        'standard finish option':  finish_options,
        'special finish option':  special_finish_options,
    },
    'lyptus': {
        'stain': [
            'caramel', 'desert mist', 'fruitwood', 'honey', 'amaretto', 'burgundy', 'walnut'
            ],
        'glaze': [
            'chocolate', 'coffee', 'linen', 'pewter', 'sueded', 'tan', 'white'
            ],    
        'style': std_door_styles,
        'standard finish option':  finish_options,
        'special finish option':  special_finish_options,
    },
    'knotty alder': { 
        'stain': [
            'alpine', 'amaretto', 'autumn', 'barley', 'black', 'blue wash', 'boulder', 'burgundy',
            'caramel', 'cinnamon', 'cream', 'desert mist', 'fruitwood', 'green wash', 'hazelnut ivory',
            'honey', 'island', 'lemon', 'london fog', 'natural maple', 'nutmeg', 'pearl', 'pecan',
            'pueblo', 'raisin', 'red wash', 'vanilla', 'walnut', 'wheat', 'wild honey',
            ],
        'glaze': [
            'chocolate', 'coffee', 'linen', 'pewter', 'sueded', 'tan', 'white'
             ],
        'style': std_door_styles,
        'standard finish option':  finish_options,
        'special finish option':  special_finish_options,
    },    
    'thermafoil': {
        'paint': [
            'antique', 'basil', 'black', 'butterscotch', 'cherries jubilee', 'clover', 'cocoa bean',
            'cocoa', 'country pebble', 'dylan green', 'fashion gray', 'fern', 'fine wine', 'forest green', 
            'goldenrod', 'indigo', 'juniper', 'misty green', 'sage', 'willow', 'shalimar', 'soft white', 
            'sunflower', 'super white', 'taupe', 'twilight blue', 'washboard',
            ],
        'style': thermafoil_or_metal_styles,
    },    
}
#    
#
range_hoods = [
    'alpine', 'athenian', 'bellini', 'biltmore', 'bordeaux', 'brussels w\ chimney', 'brussels w\o chimney', 
    'buckingham', 'cottage', 'elite', 'florentine', 'french country w\ chimney', 'french country w\o chimney', 
    'grand marquis', 'grenada', 'legacy', 'range door cabinet angled',
    'regency', 'restoration', 'seville', 'the ritz', 'vanderbilt', 'windsor house',
    ]
#    
mouldings = [
    'Crown', 'Starter', 'Spindle Rail', 'Light', 'Rail', 'Base', 'Toe Kick', 'Soffit', 'Subrail',
    'Carved', 'Accent', 'Egg & Dart', 'Dentil', 'Rope', 'Batten', 'Scribe', 'Shoe', 'Inside Corner',
    'Outside Corner', 'Half Round', 'Third Round', 'Pilaster',
    ]
    
decorative_accents = [

]

accessories = [

]