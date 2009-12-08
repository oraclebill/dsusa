keyname = 'executive'
catalog_name = 'Executive Kitchens'
line_name = 'Executive Kitchens'
logo_path = 'media/manufacturers/executive/executive.png'


product_lines = ['Executive', 
                 'Bellini', 
                 'Biltmore'] # , 'Impact']   
#
primary_finish_types = ['paint', 'stain']
finish_option_types = ['glaze', 'standard finish option', 'special finish option']
#
##
#
_std_door_styles = ['Bali', 'Bel Air', 'Biltmore Estate', 'Biltmore Manor', 'Biltmore Vineyard', 'Boca', 'Bombay', 'Brittany', 'Broadway', 'Camelot', 'Camelot Beaded', 'Charleston', 'Charleston Reversed', 'Contemporary Slab', 'Cumberland', 'Georgetown', 'Harvest', 'Harvest Reversed', 'Hilton', 'Huntington', 'Lattice', 'Louvre Solid', 'Louvre Vented', 'Midtown', 'Normandy', 'Plaza', 'Quinta', 'Rockefeller', 'Romanesque', 'Saratoga', 'Shaker 1/4 Beaded', 'Shaker 3', 'Shaker 3 Reversed', 'Shaker 4', 'Shaker Double', 'Shaker Single', 'Shaker Solid Beaded', 'Tiffany', 'Traditional', 'Traditional Beaded', 'Traditional Reversed', 'Tuscany', 'Villa', 'Williamsburg', 'Wood Veneer']
_thermafoil_or_metal_styles = ['Allegro', 'Alpha', 'Beta', 'Chateau', 'Classic Shaker', 'Cosmos', 'Dakota', 'Designer', 'Euro', 'Gamma', 'Glamour', 'Loft', 'Milano', 'New Yorker', 'Omega', 'Revere', 'Sahara', 'Shaker Beaded', 'Slab Mdf', 'Tempo', 'Traditional Shaker', 'Ultra', 'Vogue Foil', 'Zephyr']
#
#
finish_options = ['Flyspeck', 'Grain Cracking', 'Heavy Rustic Distressing', 'Lite Weathered Distressing', 'Low Sheenrandom Scraped Edges', 'Rub Thru', 'Spot Crackle', 'Wormhole']
special_finish_options = ['Biltmore Finishes', 'Brushed Glaze', 'Island Finish']
#   
door_info = {
    'maple': { 
        'stain': [
    		'Amaretto', 'Autumn', 'Barley', 'Black', 'Blue Wash', 'Burgundy', 'Caramel', 'Cinnamon',
            'Cream', 'Desert Mist', 'Fruitwood', 'Green Wash', 'Hazelnut Ivory', 'Honey', 'Island',
            'Lemon', 'London Fog', 'Natural Maple', 'Nutmeg', 'Pearl', 'Pecan', 'Raisin', 
            'Red Wash', 'Vanilla', 'Walnut', 'Wheat', 'Wild Honey',
            ],
        'glaze': ['Chocolate', 'Coffee', 'Linen', 'Pewter', 'Sueded', 'Tan', 'White'],
        'style': _std_door_styles,
        'standard finish option':  finish_options,
        'special finish option':  special_finish_options,
    },
    'cherry': { 
        'stain' : ['Cherry Cafe', 'Cherry Espresso', 'Cherry Merlot', 'Cherry Mocha', 'Cherry Moroccan', 'Cherry Port', 'Cherry Spice', 'Natural Cherry'],
        'glaze': ['Chocolate', 'Coffee', 'Linen', 'Pewter', 'Sueded', 'Tan', 'White'],
        'style': _std_door_styles,
        'standard finish option':  finish_options,
        'special finish option':  special_finish_options,
    },
    'lyptus': {
        'stain': ['Amaretto', 'Burgundy', 'Caramel', 'Desert Mist', 'Fruitwood', 'Honey', 'Walnut'],
        'glaze': ['Chocolate', 'Coffee', 'Linen', 'Pewter', 'Sueded', 'Tan', 'White'],    
        'style': _std_door_styles,
        'standard finish option':  finish_options,
        'special finish option':  special_finish_options,
    },
    'knotty alder': { 
        'stain': ['Alpine', 'Amaretto', 'Autumn', 'Barley', 'Black', 'Blue Wash', 'Boulder', 'Burgundy', 'Caramel', 'Cinnamon', 'Cream', 'Desert Mist', 'Fruitwood', 'Green Wash', 'Hazelnut Ivory', 'Honey', 'Island', 'Lemon', 'London Fog', 'Natural Maple', 'Nutmeg', 'Pearl', 'Pecan', 'Pueblo', 'Raisin', 'Red Wash', 'Vanilla', 'Walnut', 'Wheat', 'Wild Honey'],
        'glaze': ['Chocolate', 'Coffee', 'Linen', 'Pewter', 'Sueded', 'Tan', 'White'],
        'style': _std_door_styles,
        'standard finish option':  finish_options,
        'special finish option':  special_finish_options,
    },    
    'thermafoil': {
        'paint': ['Antique', 'Basil', 'Black', 'Butterscotch', 'Cherries Jubilee', 'Clover', 'Cocoa', 'Cocoa Bean', 'Country Pebble', 'Dylan Green', 'Fashion Gray', 'Fern', 'Fine Wine', 'Forest Green', 'Goldenrod', 'Indigo', 'Juniper', 'Misty Green', 'Sage', 'Shalimar', 'Soft White', 'Sunflower', 'Super White', 'Taupe', 'Twilight Blue', 'Washboard', 'Willow'],
        'style': _thermafoil_or_metal_styles,
    },    
}
#    
#
range_hoods = ['Alpine', 'Athenian', 'Bellini', 'Biltmore', 'Bordeaux', 'Brussels W\\ Chimney', 'Brussels W\\O Chimney', 'Buckingham', 'Cottage', 'Elite', 'Florentine', 'French Country W\\ Chimney', 'French Country W\\O Chimney', 'Grand Marquis', 'Grenada', 'Legacy', 'Range Door Cabinet Angled', 'Regency', 'Restoration', 'Seville', 'The Ritz', 'Vanderbilt', 'Windsor House']
#    
mouldings = ['Crown', 'Starter', 'Spindle Rail', 'Light', 'Rail', 'Base', 'Toe Kick', 'Soffit', 'Subrail', 'Carved', 'Accent', 'Egg & Dart', 'Dentil', 'Rope', 'Batten', 'Scribe', 'Shoe', 'Inside Corner', 'Outside Corner', 'Half Round', 'Third Round', 'Pilaster']
    
decorative_accents = [

]

accessories = [

]
