'''
Created on Jan 15, 2010

@author: bjones
'''

#import pymongo


class Message(object):
    
    def __init__(self, id, date, sender, subject):
        self.id = id
        self.date = date
        self.sender = sender
        self.subject = subject
        self.children = []
            
    def add_reply(self, related_message):
        self.children.append(related_message)
    
    def replies(self):
        for m in self.children:
            yield m
            
                
class DesignPackage(object):
    '''
    A design package encapsulates the fulfillment of a design request. It contains a reference to the 
    originating request/order, a version number, and date received, Optionally it will contain additional 
    metadata, such as designer name/id, etc.
    
    It contains a set of files sent by a design organization to a user
    '''
    class Const:
        OPEN, CLOSED, DELETED = 'OPEN', 'CLOSED', 'DELETED'
        FULL, DELTA = 'FULL', 'DELTA'

    def __init__(self):
        '''
        Constructor
        '''
        self.status = self.Const.OPEN
        self.order_id, self.related_package_id, self.sequence_num = None, None, 0
        self.creator, self.created_on = None, None
        self.designer = None
        self.comments = []
        self.files = []
        
    def add_file(self, file, type):
        pass
    
    def mark_complete(self):
        self.status = self.Const.CLOSED
        
    @staticmethod
    def get_package_by_id(package_id):
        pass
    
    @staticmethod
    def get_packages_for_order(order_id):
        pass
    
    @staticmethod
    def get_latest_delivered_package_for_order(order_id):
        pass
    
    @staticmethod
    def get_current_working_package_for_order(order_id):
        pass
    
    @staticmethod
    def get_open_packages(filter=None):
        pass
    
        