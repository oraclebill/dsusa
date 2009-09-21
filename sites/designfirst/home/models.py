import settings
from datetime import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

from designfirst.product.models  import PriceSchedule

class IllegalState(Exception):
    pass

# Constants and Validation Data

DIMENSION_UNIT_CHOICES = (('IN', "inches"), ('CM', "centimeters"), ('O', "other"))


class Account(models.Model):
    """
    An abstract base class for all account objects.
    
    
    """
    # class Meta:
    #     abstract = True
        
    ACCOUNT_STATUSES = ( ('P', 'Pending'), ('A', 'Active'), 
                         ('S', 'Suspended'), ('C','Cancelled'), ('O', 'Archived' ))
    status  = models.CharField(max_length=3, default="ACT", choices=ACCOUNT_STATUSES)
    company_name = models.CharField(max_length=50)
    company_address_1 = models.CharField(max_length=40, blank=True, null=True)
    company_address_2 = models.CharField(max_length=40, blank=True, null=True)
    company_city = models.CharField(max_length=10, blank=True, null=True)
    company_state = models.CharField(max_length=2, blank=True, null=True)
    company_zip4 = models.CharField(max_length=10, blank=True, null=True)
    company_phone = models.CharField(max_length=20, blank=True)
    company_fax = models.CharField(max_length=20, blank=True)
    company_email = models.EmailField()
    
    def __unicode__(self):
        return self.company_email
    
    
class DealerAccount(Account):
    """
    An individual or enterprise that purchases services from DesignFirst.
    
    Customer entities are created through a registration process. Once customers
    are registered they are given the ability to create and modify new orders, and to 
    review the status of any orders that they have created. 
    """
                                
    default_measure_units = models.CharField(max_length=3, choices=DIMENSION_UNIT_CHOICES)
    credit_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_sheet = models.ForeignKey(PriceSchedule,blank=True,null=True)
    
    def __unicode__(self):
        return self.company_name


class UserProfile(models.Model):
    """
    Site profile associating this user with either a customer account or designer profile.
    
    Customer profile is a linking mechanism. It identifies usertype which will determine which core profile
    object contains that profiles' defining information. 
    """
    user = models.ForeignKey(User, unique=True)
    usertype = models.CharField(max_length=10, choices=[('designer', 'Designer'), ('dealer','Dealer'),], default='dealer')
    account = models.ForeignKey(Account)
    
    def __unicode__(self):
        return '%s @ %s' % (self.user, self.account) 

class DesignOrder(models.Model):
    """
    A collection of product selections and associated metadata, created by a 
    Customer with the intent of purchase
    
    TODO: make get_absolute_url work..
    """
    
    PAYMENT_CHOICES = (
        ('AUTO', 'Automatic Submission'), 
        ('APPR', 'Require Approval')
    )
    
    DELIVERY_OPTIONS = (
        (1,'Color Design Views'), 
        (2,'Elevations'), 
        (3,'Quote Cabinet List'), 
    )
    
    STATUS_CHOICES = (
        ("DLR", "Dealer Editing" ),
       # ("SR", "Dealer Submission Ready" ), # logical state... is_valid & ! submitted
        ("SUB", "Submitted" ),
        ("ASG", "Assigned" ),
       # ("WK", "Working" ),
        ("RCL", "Requires Clarification" ),
       # ("RR", "Designer Review Ready" ),
        ("CMP", "Designer Completed" ),
        ("ACC", "Dealer Accepted" ),
        ("REJ", "Dealer Rejected" ),
        ("WTH", "Dealer Withdrawn" ),
    )
    
    REVIEW_RATING_CHOICES = [x for x in enumerate(
        ['unacceptably bad', 'barely acceptable', 'fair', 'good', 'very good', 'excellent', 'astonishingly superior'])]

    client_account  = models.ForeignKey(Account, related_name='created_orders',verbose_name='Customer Account')
#TODO: add client contact info for user who entered order
#    client_contact  = models.ForeignKey(User, related_name='created_orders',verbose_name='Client Contact', null=True, blank=True)
    project_name    = models.CharField(max_length=25, verbose_name='Project')
    description     = models.TextField(null=True, blank=True, verbose_name='Description')
    status          = models.CharField(max_length=3, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    cost            = models.PositiveSmallIntegerField(default=1, verbose_name='Design Price')
    designer        = models.ForeignKey(User, blank=True, null=True, related_name='serviced_orders')
    
    # format options
    color_views     = models.BooleanField(blank=True, verbose_name='Color Views')
    elevations      = models.BooleanField(blank=True, verbose_name='Elevations')
    quote_cabinet_list = models.BooleanField(blank=True, verbose_name='Quoted Cabinet List')

    # cabinetry options
    cabinet_manufacturer = models.CharField(max_length=20, blank=True, null=True, 
        verbose_name='Manufacturer')
    cabinet_door_style = models.CharField(max_length=20, blank=True, null=True, 
        verbose_name='Door Style')
    cabinet_wood = models.CharField(max_length=20, blank=True, null=True, 
        verbose_name='Wood')
    cabinet_stain = models.CharField(max_length=20, blank=True, null=True, 
        verbose_name='Stain')
    cabinet_finish = models.CharField(max_length=20, blank=True, null=True, 
        verbose_name='Other Finish')
    cabinet_finish_options =  models.CharField(max_length=20, blank=True, null=True, 
        verbose_name='Special Options')
    cabinetry_notes =  models.CharField(max_length=20, blank=True, null=True, 
        verbose_name='Notes')

    # door and drawer hardware
    include_hardware    = models.BooleanField(blank=True, verbose_name='Include Hardware Details?')
    door_hardware       = models.CharField(max_length=20, blank=True, null=True, verbose_name='Doors')
    drawer_hardware     = models.CharField(max_length=20, blank=True, null=True, verbose_name='Drawers')

    # mouldings
    ceiling_height = models.CharField(max_length=6, blank=True, null=True)
    crown_mouldings = models.CharField(max_length=20, blank=True, null=True)
    skirt_mouldings = models.CharField(max_length=20, blank=True, null=True)
    soffits = models.BooleanField(blank=True)
    soffit_height = models.IntegerField(blank=True, null=True) # for now, number of 1/8 inches.. 
    soffit_width  = models.IntegerField(blank=True, null=True) # for now, number of 1/8 inches.. 
    soffit_depth  = models.IntegerField(blank=True, null=True) # for now, number of 1/8 inches.. 

    # dimensions
    stacked_staggered = models.BooleanField(default=False)
    wall_cabinet_height = models.CharField(max_length=8, blank=True, null=True, 
        choices=(('30', '30"'), ('36', '36"'), ('40.5', '40 1/2"')))
    vanity_cabinet_height =  models.CharField(max_length=8, blank=True, null=True, 
        choices=(('31.625', '31 5/8"'), ('34.625', '34 5/8"')))
    vanity_cabinet_depth = models.CharField(max_length=8, blank=True, null=True,
        choices=(('21', '21"'), ('18', '18"'), ('16', '16"')))
        
    # corner cabinet options
    corner_cabinet_base_bc = models.BooleanField()
    corner_cabinet_base_bc_direction = models.CharField(max_length=1, blank=True, null=True,
        choices=(('L','Left'), ('R', 'Right')))
    corner_cabinet_wall_bc = models.BooleanField()
    corner_cabinet_wall_bc_direction = models.CharField(max_length=1, blank=True, null=True,
        choices=(('L','Left'), ('R', 'Right')))
        
    # TODO: island / peninsula
    island_peninsula_option = models.CharField( max_length=1, blank=True, null=True,
        choices=(('S','Single Height'), ('R', 'Raised Eating Bar')))
        
    # other considerations
    countertop_option = models.CharField( max_length = 20, blank=True, null=True )
    backsplash = models.BooleanField(default=False)
    toekick = models.BooleanField(default=False)

    # organization
    lazy_susan = models.BooleanField(default=False)
    slide_out_trays = models.BooleanField(default=False)
    waste_bin = models.BooleanField(default=False)
    wine_rack = models.BooleanField(default=False)
    plate_rack = models.BooleanField(default=False)
    appliance_garage = models.BooleanField(default=False)

    # miscellaneous
    corbels_brackets = models.BooleanField(default=False)
    valance = models.BooleanField(default=False)
    legs_feet = models.BooleanField(default=False)
    glass_doors = models.BooleanField(default=False)
    range_hood = models.BooleanField(default=False)
    posts = models.BooleanField(default=False)
    
    # notes
    miscellaneous_notes = models.TextField(blank=True, null=True)
    
    # diagrams
    client_diagram = models.FileField(upload_to='inbound',null=True, blank=True)
#TODO: add
#    client_diagram_recieved = models.DateTimeField(null=True,blank=True)
    client_diagram_source = models.CharField(max_length=3,null=True, blank=True, 
        choices=(('UPL', 'Upload'), ('FAX', 'Fax')), default='UPL')
    client_diagram_notes = models.TextField(null=True, blank=True)
    designer_package = models.FileField(upload_to='outbound',null=True, blank=True)
    designer_package_notes = models.TextField(null=True, blank=True)
    
    # post delivery ratings
    client_review_rating = models.SmallIntegerField(null=True, blank=True, 
        choices=REVIEW_RATING_CHOICES, verbose_name='Rating')
    client_review_notes = models.TextField(null=True, blank=True, verbose_name='Review Notes')
    client_notes = models.TextField(null=True,blank=True)
    designer_notes = models.TextField(null=True,blank=True)
    
    # tracking information - system managed
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    modified_by = models.CharField(max_length=35, null=True, blank=True)

    visited_status  = models.IntegerField(default=0, editable=False)
    valid_status    = models.IntegerField(default=0, editable=False)

    submitted = models.DateTimeField(null=True,blank=True)
    assigned = models.DateTimeField(null=True,blank=True)
    projected = models.DateTimeField(null=True,blank=True)
    completed = models.DateTimeField(null=True,blank=True)
    closed = models.DateTimeField(null=True,blank=True)

    tracking_notes = models.TextField(null=True,blank=True)
    
    # fields considered 'optional'  #TODO this is primarily a display thing.. move it
    display_as_optional = [ 
        corner_cabinet_base_bc, corner_cabinet_base_bc_direction, corner_cabinet_wall_bc,
        corner_cabinet_wall_bc_direction, island_peninsula_option, countertop_option, backsplash,
        toekick, lazy_susan, slide_out_trays, waste_bin, wine_rack, plate_rack, appliance_garage,
        corbels_brackets, valance, legs_feet, glass_doors, range_hood, posts,
    ]        

    #
    # some convenience functions
    #
    def client_editable(self):
        return 'DLR' == self.status
        
    def minimally_valid(self):
        return True
        
    def is_submittable(self):
        if 'DLR' == self.status and self.client_diagram and (self.visited_status & 0x000f) >0:
#TODO            and self.validated_status & 0x3          
            return True       
        else:
            return False
        
    def save(self, a=False, b=False):
        if False:
            pass
        super(DesignOrder, self).save(a,b)
    
    
    def is_assigned(self):
        return self.status == 'ASG'
        
    def is_completed(self):
        return self.status == 'CMP'
        
    def is_accepted(self):
        return self.status == 'ACC'
        
    def is_rejected(self):
        return self.status == 'REJ'
        

    def dealer_submit(self):
        """
        Call this when a dealer submits an order to designers, or when a diagram is added to an 
        otherwise 'ready' order.
        
        TODO
        """
        # validate submission conditions
        if not self.is_submittable(): 
            raise IllegalState( "illegal status - cannot submit order in %s status" 
                            % self.status )

        # update status
        from datetime import datetime
        self.status = 'SUB'
        self.submitted = datetime.now()
        
        # save model
        self.save()
        
        # generate status change notification (or just send mail)
        # TODO: enqueue mail for sending.. 
        # TODO: remove hardcoded (demo) email addresses
        from django.core.mail import send_mail
        send_mail( 
            'New order submitted by %s on %s' % (self.client_account,self.submitted),
            """\
            \n\n\n
            The following order has been submitted for design creation:
            
            Order ID: %s
            Project Name: %s
            Notes:  
            
            
            """ % (self.id, self.project_name),
            settings.MAIL_SYSTEM_REPLYTO_ADDRESS,
            [ settings.DEMO_MAIL_DESIGNER_ADDRESS, settings.MAIL_SYSTEM_NOTIFY_ADDRESS ],
            False
        )    
        
        # TODO: send notification email to dealer on submit in case of auto-submissions
        
    def dealer_accept(self):
        pass
        
    def dealer_reject(self):
        pass
        
        
        
    def assign_designer(self, designer, allow_reassign=False):
        
        if self.designer and not allow_reassign:
            raise IllegalState('Cannot reassign order - current designer %d' % self.designer)
        self.status = 'ASG'
        self.designer = designer
        self.assigned = datetime.now()
#        self.tracking_notes = self.tracking_notes + '> assigned designer %s\n' % self.designer
        self.save() 
        
    def designer_complete(self, designer, notes=None):

        if not self.designer == designer:
            raise IllegalState, 'Designer assigned to order (%s) is different than designer completing order (%s)' \
                % (self.designer, designer)
            
        if not self.status == 'ASG':
            raise IllegalState, 'Order must be in "Assigned" state - current status is "%s"' % self.get_status_display()

        self.status = 'CMP'
        self.completed = datetime.now()
        self.designer_notes = notes
        self.save()
                
    def get_absolute_url(self):
        return reverse('home.edit_order_detail')
                
    def __unicode__(self):
        return "Order #%s for %s [%s] - %s" % (self.id, self.client_account.company_name, self.status, self.description)



class OrderAppliance(models.Model):
    
    APPLIANCE_CHOICES = (
        ( "REF", "Refrigerator" ), 
        ( "SIN", "Sink" ),
        ( "MIC", "Microwave" ),
        ( "RAN", "Range" ),
        ( "COO", "Cook Top*" ),
        ( "DIS", "Dishwasher" ),
        ( "SIN", "Single Oven*" ),
        ( "DOU", "Double Oven*" ),
        ( "OTH", "Other" ),
    )

    APPLIANCE_CHOICE_OPTIONS = {
        "REF": ["Double Door", "Single Door, Left", "Single Door, Right"], 
        "MIC": ["Free Standing", "Built-in*", "Over Range"], 
        "RAN": ["Slide In", "Raised Back"], 
        "COO": ["Front Controls", "Top Controls"], 
        "SIN": ["Single", "1 1/2", "Double"], 
    }
    
    order = models.ForeignKey(DesignOrder, editable=False)
    appliance_type = models.CharField(max_length=3, choices=APPLIANCE_CHOICES)
    description = models.CharField(max_length=20, blank=True)  # only needed when type = other
    height = models.IntegerField()
    width = models.IntegerField()
    depth = models.IntegerField()
    options = models.CharField(max_length=240, blank=True) # comma separated option list

    # class Meta:
    #     unique_together = (("order", "appliance_type"),)
        
    def __unicode__(self):
        return "%s: [%s x %s x %s]" % (self.appliance_type, self.height, self.width, self.depth)


class OrderDiagram(models.Model):
    order = models.ForeignKey(DesignOrder, editable=False)
    document_id = models.CharField(max_length=24) # speculation: efax correlation id?
    recieved_from = models.CharField(max_length=3, choices=(("EFX", "eFax"), ("UPL","Upload"), ("MAN","Manual")))
    created = models.DateTimeField(auto_now=True)
    filename = models.FileField(upload_to='.')

    class Meta:
        unique_together = (("order", "document_id"),)
            
    def __unicode__(self):
        return "diagram '%s' for order %s" % (self.document_id, self.order.id) 


class OrderNotes(models.Model):
    order = models.ForeignKey(DesignOrder)
    sequence = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    
    
class Transaction(models.Model): # TODO --> invoice becomes transaction
    account = models.ForeignKey(DealerAccount)
    debit_or_credit = models.CharField(max_length=1, choices=(('D', 'Debit'), ('C', 'Credit')))
    trans_type = models.CharField(max_length=1, choices=(('C', 'Credits'), ('D', 'Dollars')))
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)



#
# signals handling
#
