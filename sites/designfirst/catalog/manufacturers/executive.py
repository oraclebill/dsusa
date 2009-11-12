product_lines = [ 
        'executive',
        'bellini',
        'biltmore',
        #'impact'  # no data...
    ]

class Executive(object):
    def get_product_lines(self):
        return product_lines;
    
#
wood_species = [
        'maple',
        'cherry',
        'lyptus',
        'knotty alder'
        'mdf',
    ]
#    
stains_by_species = {
    'maple': [
		'Amaretto', 
		'Autumn', 
		'Barley', 
		'Black', 
		'Blue Wash', 
		'Burgundy', 
		'Caramel', 
		'Cinnamon', 
		'Cream', 
		'Desert Mist', 
		'Fruitwood', 
		'Green Wash',
		'Hazelnut Ivory',
		'Honey', 
		'Island', 
		'Lemon', 
		'London Fog', 
		'Natural Maple', 
		'Nutmeg', 
		'Pearl', 
		'Pecan', 
		'Raisin', 
		'Red Wash', 
		'Vanilla', 
		'Walnut',
		'Wheat',
		'Wild Honey',
        ],
    'cherry': [
        'natural cherry',
        'cherry cafe',
        'cherry merlot',
        'cherry spice',
        'cherry espresso',
        'cherry mocha',
        'cherry moroccan',
        'cherry port',
        ],
    'lyptus': [
        'caramel',
        'desert mist',
        'fruitwood',
        'honey',
        'amaretto',
        'burgundy',
        'walnut'
        ],
    'knotty alder': [
        'alpine',
        'amaretto',
        'autumn',
        'barley',
        'black',
        'blue wash',
        'boulder',
        'burgundy',
        'caramel',
        'cinnamon',
        'cream',
        'desert mist',
        'fruitwood',
        'green wash',
        'hazelnut ivory',
        'honey',
        'island',
        'lemon',
        'london fog',
        'natural maple',
        'nutmeg',
        'pearl',
        'pecan',
        'pueblo',
        'raisin',
        'red wash',
        'vanilla',
        'walnut',
        'wheat',
        'wild honey',
        ]
    }
#    
paints_by_species = {
    'mdf': [
        'antique', 
        'basil', 
        'black', 
        'butterscotch',
        'cherries jubilee', 
        'clover', 
        'cocoa bean', 
        'cocoa', 
        'country pebble', 
        'dylan green', 
        'fashion gray', 
        'fern', 
        'fine wine',
        'forest green', 
        'goldenrod', 
        'indigo', 
        'juniper', 
        'misty green', 
        'sage', 'willow',
        'shalimar', 
        'soft white', 
        'sunflower', 
        'super white', 
        'taupe',
        'twilight blue',
        'washboard',
    ]}    
#
glazes_by_species = {
    'maple': [
        'chocolate', 
        'coffee', 
        'linen', 
        'pewter', 
        'sueded', 
        'tan', 
        'white'
        ],
    'cherry': [
        'chocolate', 
        'coffee', 
        'linen', 
        'pewter', 
        'sueded', 
        'tan', 
        'white'
        ],
    'lyptus': [
        'chocolate', 
        'coffee', 
        'linen', 
        'pewter', 
        'sueded', 
        'tan', 
        'white'
         ],    
    'knotty alder': [
        'chocolate', 
        'coffee', 
        'linen', 
        'pewter', 
        'sueded', 
        'tan', 
        'white'
         ]    
    }                
#
standard_finish_options = [
    'flyspeck',
    'grain cracking',
    'heavy rustic distressing',
    'lite weathered distressing',
    'low sheen'
    'random scraped edges',
    'rub thru',
    'spot crackle',
    'wormhole',
    ]
#
extra_specialty_finish_options = {
    'all': [
        'biltmore finishes',
        'brushed glaze',
        'island finish',
        ]
    }
    
door_styles = {
    'all': [
        'bali', 
        'bel air', 
        'bitlmore estate', 
        'bitlmore manor', 
        'bitlmore vineyard', 
        'boca', 
        'bombay', 
        'brittany', 
        'broadway', 
        'camelot', 
        'camelot beaded', 
        'charleston', 
        'charleston reversed', 
        'contemporary slab', 
        'cumberland', 
        'georgetown', 
        'harvest', 
        'harvest reversed', 
        'hilton', 
        'huntington', 
        'lattice', 
        'louvre solid', 
        'louvre vented', 
        'midtown', 
        'normandy', 
        'plaza', 
        'quinta', 
        'rockefeller', 
        'romanesque', 
        'saratoga', 
        'shaker 1/4” beaded', 
        'shaker 3”', 
        'shaker 3” reversed', 
        'shaker 4”', 
        'shaker double', 
        'shaker single', 
        'shaker solid beaded', 
        'tiffany', 
        'traditional', 
        'traditional beaded', 
        'traditional reversed', 
        'tuscany', 
        'villa', 
        'williamsburg', 
        'wood veneer', 
    ],    
    'thermafoil_or_metal': [
        'allegro', 
        'alpha', 
        'beta', 
        'chateau', 
        'classic shaker', 
        'cosmos', 
        'dakota', 
        'designer', 
        'euro', 
        'gamma', 
        'glamour', 
        'loft', 
        'milano', 
        'new yorker', 
        'omega', 
        'revere', 
        'sahara', 
        'shaker beaded', 
        'slab mdf', 
        'tempo', 
        'traditional shaker', 
        'ultra', 
        'vogue foil', 
        'zephyr', 
        ],
    }

range_hoods = [
    'alpine', 
    'athenian', 
    'bellini', 
    'biltmore', 
    'bordeaux', 
    'brussels w\ chimney', 
    'brussels w\o chimney', 
    'buckingham', 
    'cottage', 
    'elite', 
    'florentine', 
    'french country w\ chimney', 
    'french country w\o chimney', 
    'grand marquis', 
    'grenada', 
    'legacy', 
    'range door cabinet angled', 
    'regency', 
    'restoration', 
    'seville', 
    'the ritz', 
    'vanderbilt', 
    'windsor house', 
    ]
    
mouldings = [
    'Crown', 
    'Starter', 
    'Spindle Rail', 
    'Light', 
    'Rail', 
    'Base', 
    'Toe Kick', 
    'Soffit', 
    'Subrail', 
    'Carved', 
    'Accent', 
    'Egg & Dart', 
    'Dentil', 
    'Rope', 
    'Batten', 
    'Scribe', 
    'Shoe', 
    'Inside Corner', 
    'Outside Corner', 
    'Half Round', 
    'Third Round', 
    'Pilaster',
    ]
    
decorative_accents = [

]

accessories = [

]