_all_manufacturers = [ 'executive', 'fieldstone' ]
_cabinet_lines = {}

                
class CabinetLine(object):
    
    def __init__(self, module):
        if type(module) == str:
            module = __import__('catalog.manufacturers.%s'%module, fromlist=[''])
        self.module = module
        self.keyname = module.keyname
        self.catalog_name = module.catalog_name
        self.line_name = module.line_name
        self.product_lines = module.product_lines
        self.door_info = module.door_info
        self.primary_finish_types = module.primary_finish_types
        self.finish_option_types = module.finish_option_types
        self.primary_finish_set = set(reduce(list.__add__, [self.get_primary_finishes(ftype) for ftype in self.primary_finish_types]))
        self.finish_options_set = set(reduce(list.__add__, [self.get_finish_options(otype) for otype in self.get_finish_option_types()]))
        
    def _get_options_for_attribute(self, attr, species=None, style=None):
        """ 
        for each attribute in the master map (door_info), returns the union of all options for that attribute.
        
        >>> cl = CabinetLine(self) 
        >>> cl.door_info = { 'test': { 'first': [1, 2, 3], 'second': [ 'x' ] }, 'test2': { 'first': [100,200,300], 'second': [ 'ecks' ] } }
        cl._all_materials('first')
        [1, 2, 3, 100, 200, 300] 
        >>> cl._all_materials('second')
        ['x', 'ecks'] 
        >>> cl._all_materials('third') 
        [] 
        """
        ret = species and self.door_info[species].get(attr,[]) or \
            list(set(reduce(list.__add__, [d.get(attr,[]) for d in self.door_info.values()])))
        return sorted(ret) 
            
    def get_door_materials(self, style=None):
        if style:
            return [key for key in self.door_info.keys() if style in self.door_info[key]['style']]
        else:
            return self.door_info.keys() #
      
    def get_primary_finish_types(self, species=None, style=None):
        if style:
            raise NotImplementedError('style query not supported')
        if species: 
            return [key for key in self.door_info[species].keys() if key in self.primary_finish_types]
        else: 
            return self.primary_finish_types[:]
    
    def get_finish_option_types(self, species=None, finish_type=None, style=None):
        if style:
            raise NotImplementedError('style query not supported')
        if finish_type:
            raise NotImplementedError('style query not supported')
        #
        if species: 
            return [key for key in self.door_info[species].keys() if key in self.finish_option_types]
        else: 
            return self.finish_option_types
    
    def get_door_styles(self, species=None ):
        return self._get_options_for_attribute('style', species)
        
    def get_primary_finishes(self, finish_type=None, species=None, style=None):
        return finish_type and self._get_options_for_attribute(finish_type, species) or \
                list(set(reduce(list.__add__, [self._get_options_for_attribute(key, species) for key in self.primary_finish_types])))
        
    def get_finish_options(self, option_type=None, species=None, style=None):
        return option_type and self._get_options_for_attribute(option_type, species) or \
                list(set(reduce(list.__add__, [self._get_options_for_attribute(key, species) for key in self.finish_options_set])))

    def logo_path(self):
        # relative to MEDIA_URL
        return getattr(self.module, 'logo_path', None)

class Catalog(dict):
    def __init__(self):
        for name in _all_manufacturers:
            cabinet_line = CabinetLine(name)
            self[cabinet_line.catalog_name] = cabinet_line 
            
    def manufacturers(self):
        return self.keys()
    
    def cabinet_line(self, name):
        return self[name]
    
def get_manufacturers():
    c = Catalog()
    return [(n,m.catalog_name) for n,m in c.items()]

