
class CabinetLine(object):
    
    def __init__(self, module):
        self.module = module
        self.primary_finish_types = module.primary_finish_types
        self.finish_option_types = module.finish_option_types
        self.finish_options = module.finish_options
        self.door_info = module.door_info
        
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
        return species and self.door_info[species].get(attr,[]) or \
            list(set(reduce(list.__add__, [d.get(attr,[]) for d in self.door_info.values()]))) 
            
    def get_door_materials(self, style=None):
        if style:
            return [key for key in self.door_info.keys() if style in self.door_info[key]['style']]
        else:
            return self.door_info.keys()
    
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
                list(set(reduce(list.__add__, [self._get_options_for_attribute(key, species) for key in self.finish_options])))

