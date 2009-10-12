import settings


from datetime import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _

from designfirst.product.models  import PriceSchedule

class IllegalState(Exception):
    pass

# Constants and Validation Data

INCH_DIMENSION='IN'
CENTIMETER_DIMENSION='CM'
OTHER_DIMENSION='O'
DIMENSION_UNIT_CHOICES = (
    (INCH_DIMENSION, _("inches")), 
    (CENTIMETER_DIMENSION, _("centimeters")), 
    (OTHER_DIMENSION, _("other")))


class Organization(models.Model):
    """
    An abstract base class for all account objects.
    
    """
    PENDING, ACTIVE, SUSPENDED, CANCELLED = ('P','A', 'S', 'C')    
    STATUS_CHOICES = ( (PENDING, _('Pending')), (ACTIVE, _('Active')),
                         (SUSPENDED, _('Suspended')), (CANCELLED, _('Cancelled')), )
                         
#     id = models.CharField(_('Organization'), primary_key=True, max_length=20,  )
    status  = models.CharField(_('Account Status'), max_length=3, default=PENDING, choices=STATUS_CHOICES)
    name = models.CharField(_('Legal Name'), max_length=50)
    address_1 = models.CharField(_('Address Line 1'), max_length=40, blank=True, null=True)
    address_2 = models.CharField(_('Address Line 2'), max_length=40, blank=True, null=True)
    city = models.CharField(_('City'), max_length=10, blank=True, null=True)
    state = models.CharField(_('State'), max_length=2, blank=True, null=True)
    zip4 = models.CharField(_('Postal Code'), max_length=10, blank=True, null=True)
    phone = models.CharField(_('Business Phone'), max_length=20, blank=True)
    fax = models.CharField(_('Business Fax'), max_length=20, blank=True)
    email = models.EmailField(_('Business Email'), )

    class Meta:
        abstract = True
                    
    def __unicode__(self):
        return self.name
    
    
class DealerOrganization(Organization):
    """
    An individual or enterprise that purchases services from DesignFirst.
    
    Customer entities are created through a registration process. Once customers
    are registered they are given the ability to create and modify new orders, and to 
    review the status of any orders that they have created. 
    """
    primary_contact = models.ForeignKey(User, verbose_name=_('Primary Contact'))                                
    account_rep     = models.CharField(_('Account Rep'), max_length=20,blank=True)
    num_locations   = models.SmallIntegerField(_('Number of Locations'))
    credit_balance  = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_sheet     = models.ForeignKey(PriceSchedule,blank=True,null=True)
    
#     def save(self):
#         super(DealerOrganization, self).save()


class UserProfile(models.Model):
    """
    Site profile associating this user with either a customer account or designer profile.
    
    Customer profile is a linking mechanism. It identifies usertype which will determine which core profile
    object contains that profiles' defining information. 
    """    
    user = models.ForeignKey(User, unique=True)
    account = models.ForeignKey(DealerOrganization)
    usertype = models.CharField(max_length=10, 
        choices=[('designer', 'Designer'), ('dealer','Dealer'),], default='dealer') # TODO: usertype is determined by 'account'

    # for profiles module
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)
        
    def __unicode__(self):
        if hasattr(self,'user') and hasattr(self, 'account'):
            return '%s @ %s' % (self.user, self.account) 
        else:
            return '[empty user profile]'

    
class DesignOrder(models.Model):
    """
    A collection of product selections and associated metadata, created by a 
    Customer with the intent of purchase
    
    """
    
    ## 
    ## Constants
    ##
    
    STATUS_CHOICES = (
        ("DLR", "Working" ),
        ("SUB", "Submitted" ),
        ("CMP", "Complete" ),
    )
    
    KITCHEN, BATH, CLOSET, DEN, OTHER = range(0,5)
    DESIGN_TYPE_CHOICES = (
        ( KITCHEN, _('Kitchen')),
        ( BATH, _('Bath')),
        ( CLOSET, _('Closet')),
        ( DEN, _('Den')),
        ( OTHER, _('Other')),
    )
    
    SMS, PHONE, FAX, IM, TWITTER_DM = range(0,5)
    NOTIFICATION_CHOICES = (
        ( SMS, _('SMS')),
        ( PHONE, _('Phone')),
        ( FAX, _('Fax')),
        ( IM, _('IM')),
        ( TWITTER_DM, _('Twitter DM')),
    )
        
    ##
    ## Fields
    ##
    
    # core order management fields
    customer        = models.ForeignKey(Organization, related_name='created_orders', verbose_name=_('Customer'))
    project_name    = models.CharField(_('Project Name'), max_length=25)  # TODO: slugify?
    design_type     = models.SmallIntegerField(_('Project Type'), max_length=10, choices=DESIGN_TYPE_CHOICES) 
    color_views     = models.BooleanField(_('Perspective Views?'), default=False)
    elevations      = models.BooleanField(_('Floorplan Elevations?'))
    price_report    = models.BooleanField(_('Cabinet Price Report'))
    source          = models.CharField(_('Order Source'), max_length=10, default='web') # or fax, or other
    entered_by      = models.CharField(_('Entered By'), max_length=25) # username or 'none' 
    received        = models.DateTimeField(_('Received On'), default=datetime.now,
        help_text=_('The date/time this order was recieved from the customer. For fax orders this is the time the fax was recieved.'))
    desired         = models.DateField(_('Desired On'), null=True, blank=True, 
        help_text=_('You can enter a desired delivery date for your design here. When your order is processed we will take this info consideration when your estimated delivery time is determined. To ensure accelerated delivery you can select the "Rush Delivery". Rush designs submitted before 1pm EST can be completed by 8am the next day.'))
    addl_notification_method = models.CharField(_('Additional Notification Method'), max_length=10, blank=True, 
        choices=NOTIFICATION_CHOICES, 
        help_text=_('In addition to the standard email notfication, you can select an additional method if your profiles contains matching contact information for one of these mechanisms.')) 
    document_reference_id = models.CharField(_('Document Reference'), max_length=30, blank=True, 
        help_text=_('The reference or document number for a source document, e.g. a faxage document id for transcoded fax orders.'))
    submitter_notes = models.TextField(_('Notes'), null=True, blank=True)
    
    # tracking information - system managed
    status          = models.CharField(_('Status'), max_length=3, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0])
    last_modified   = models.DateTimeField(auto_now=True, null=True, blank=True)
    last_modified_by = models.CharField(max_length=35, blank=True)

    submitted = models.DateTimeField(null=True, blank=True)
    assigned = models.DateTimeField(null=True, blank=True)
    projected = models.DateTimeField(null=True, blank=True)
    completed = models.DateTimeField(null=True, blank=True)
    closed = models.DateTimeField(null=True, blank=True)


    ###
    ###  BEGIN DESIGN OPTIONS
    ###

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
            'New order submitted by %s on %s' % (self.entered_by,self.submitted),
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
        
        if self.designer and designer and not designer.id == self.designer.id and not allow_reassign:
            raise IllegalState('Cannot reassign order - current designer %s' % self.designer)
        self.status = 'ASG'
        self.designer = designer
        self.assigned = datetime.now()
#        self.tracking_notes = self.tracking_notes + '> assigned designer %s\n' % self.designer
        self.save() 
        
    def designer_complete(self, designer, notes=None):

        if not self.designer == designer or designer.is_staff:
            raise IllegalState, 'Designer assigned to order (%s) is different than designer completing order (%s)' \
                % (self.designer, designer)
            
        if not self.status == 'ASG':
            raise IllegalState, 'Order must be in "Assigned" state - current status is "%s"' % self.get_status_display()

        if not self.orderattachment_set.filter(org__exact=designer.get_profile().account):
            raise IllegalState, 'Order must have at least one attachment from designer''s organization to complete.' 

        self.status = 'CMP'
        self.completed = datetime.now()
        self.designer_notes = notes
        self.save()
                
    def get_absolute_url(self):
        return reverse('home.edit_order_detail')
                
    def __unicode__(self):
        return "Order #%s [%s] (%s)" % (self.id, self.project_name, self.status)



class OrderAttachment(models.Model):
    TYPE_CHOICES = enumerate([ '20/20 KIT File', 'PDF - Color Views', 'PDF - Elevations', 'Other' ])
    SOURCE_CHOICES = enumerate([ 'Client', 'Design Org', 'Admin', 'Other' ])
    METHOD_CHOICES = enumerate([ 'Web', 'Fax', 'Email', 'Admin', 'Other' ])
    
    # TODO: make pk?, fax document id, or uuid if not fax
    document_id = models.CharField(_('Document ID'),max_length=24, blank=True) 
    document = models.FileField(_('File'), upload_to='files/attachments/%Y/%m/%d',)
    order = models.ForeignKey(DesignOrder, null=True, blank=True)
    source = models.SmallIntegerField(_('Source Organization Type'), choices=SOURCE_CHOICES) # todo: delete - redundant with 'org.ttype'
    doctype = models.SmallIntegerField(_('Document Type'), choices=TYPE_CHOICES)
    method = models.SmallIntegerField(_('Uploaded Using'), choices=METHOD_CHOICES )
    user = models.ForeignKey(User, null=True, blank=True)
    org = models.ForeignKey(Organization, null=True, blank=True)
    timestamp = models.DateTimeField(_('Upload Timestamp'), auto_now=True)
    
    
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

class OrderNotes(models.Model):
    order = models.ForeignKey(DesignOrder)
    sequence = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    
    
class Transaction(models.Model): # TODO --> invoice becomes transaction
    account = models.ForeignKey(DealerOrganization)
    debit_or_credit = models.CharField(max_length=1, choices=(('D', 'Debit'), ('C', 'Credit')))
    trans_type = models.CharField(max_length=1, choices=(('C', 'Credits'), ('D', 'Dollars')))
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=32)
    timestamp = models.DateTimeField(auto_now_add=True)



#
# signals handling
#
