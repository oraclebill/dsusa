# non-relational data model for df - om

class ApplianceType(object):
    def __init__(self, name, is_cutout = False, options=[]):
        self.name = name
        self.cutout = is_cutout
        self.option_names = options

appliance_types = [
class Appliance(object):
    def __init__(self, name, is_cutout = False, options=[]):
        self.name = name
        self.cutout = is_cutout
        self.option_names = options

class Appliance(object):
    def __init__(self, appliance_type):        
        options = {}
        self.width, self.height, self.depth = (None,None,None)

class Microwave(Appliance):
    def __init__(self):
        super("microwave", { "free standing"
                           
