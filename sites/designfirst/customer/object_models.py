
class ApplianceType(object):
    def __init__(self, name, is_cutout = False, options=[]):
        self.name = name
        self.cutout = is_cutout
        self.option_names = options

class Appliance(object):
    def __init__(self, name, is_cutout = False, options=[]):
        self.name = name
        self.cutout = is_cutout
        self.option_names = options

