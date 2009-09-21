

class Order(object):
    def __init__(self, id):
        self.id = id
        
        
class DesignRequest(object):
    """docstring for DesignRequest"""
    
    SILVER      = 'silver'
    GOLD        = 'gold'
    PLATINUM    = 'platinum'
    
    def __init__(self, id, type=DesignRequest.SILVER, project=None):
        self.id = id
        self.type = type
        self.project = project
        self.selections = []
            
            
class Selections(object):
    def __init__(self, state=None):
        if not state:
            self.selection_options = []
            self.selection_values = {}
        else:
            self.unpack_group_state(state)

    def unpack_group_state(self,state):
        pass
        
    def register(self,group):
        self.groups.append(group)
        
    def is_valid(self):
        for i in xrange(len(self.selections)):
            if not self.groups[i].is_valid():
                return False
        return True
        
    def is_complete(self):
         required = [item for item in selection_]
                        
class SelectionGroup(object):
    def __init__(self, name, required=False):
        self.name = name
        self.items = []
        
    def add(self, item):
        
        
class SelectionItem(object):
    """docstring for SelectionItem"""
    def __init__(self, name, type='char', length='20', choices=None, default=None, required=False, group_required=False):
        self.attrs = locals()
    
    
        
            
    
