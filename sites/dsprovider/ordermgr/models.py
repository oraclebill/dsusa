from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from datetime import datetime


DESIGN_UPLOAD_LOCATION = 'design-uploads/'  ## TODO: add strftime

# delivery option choices
DO_COLORVIEWS, DO_ELEVATIONS, DO_CABINETQUOTE = range(3)

# status (tbd)
STATUS_NEW, STATUS_ASSIGNED, STATUS_COMPLETED, STATUS_ACCEPTED, \
    STATUS_REJECTED, STATUS_NEW_CLARIFY, STATUS_ASSIGNED_CLARIFY = range(7)


class UserProfile(models.Model):
    """
    A profile for users that of the designer portal.
    """
    user = models.ForeignKey(User, primary_key=True)
    is_manager = models.BooleanField(_('Special Admin Status?'), default=False)


class DesignOrderManager(models.Manager):

    class Meta:
        model = 'DesignOrder'


class DesignOrder(models.Model):
    """
    A collection of product selections and associated metadata, created by a
    Customer with the intent of purchase

    TODO: make get_absolute_url work..
    """

    DELIVERY_OPTIONS = (
        (DO_COLORVIEWS, _('Color Design Views')),
        (DO_ELEVATIONS, _('Elevations')),
        (DO_CABINETQUOTE, _('Quote Cabinet List')),
    )

    STATUS_CHOICES = (
        (STATUS_NEW, _("New")),
        (STATUS_NEW_CLARIFY, _("New Clarify")),
        (STATUS_ASSIGNED, _("Assigned")),
        (STATUS_ASSIGNED_CLARIFY, _("Assigned Clarify")),
        (STATUS_COMPLETED, _("Completed")),
        (STATUS_ACCEPTED, _("Accepted")),
        (STATUS_REJECTED, _("Rejected")),
    )

    id = models.CharField(_('Order ID'), max_length=20, primary_key=True,
        help_text=_('A unique identifier for this order')) # also slug?

    source = models.CharField(_('Order Source'), max_length=10, null=True, blank=True,
        help_text=_('A code indicating the source of the order. This is an organization such as TCMG'))

    source_id = models.CharField(_('Source Tracking Code'), max_length=80, null=True, blank=True,
        help_text=_('A tracking ID supplied by the submitter. Not used internally.'))

    description = models.TextField(_('Description'), null=True, blank=True,
        help_text=_('A human readable description provided by the design client.'))

    status = models.SmallIntegerField(_('Status'), default=STATUS_NEW, choices=STATUS_CHOICES,
        help_text=_('The current status of this order within the providers externally visible workflow.'))

    designer = models.CharField(_('Designer'), max_length=40, null=True, blank=True,
        help_text=_('The name of the currently assigned designer.'))

    arrived = models.DateTimeField(_('Arrival Timestamp'), default=datetime.now,
        help_text=_('A timestamp of when this order was created.'))
    completed = models.DateTimeField(_('Completion Timestamp'),
        null=True, blank=True,
        help_text=_('A timestamp of when this order was completed.'))

    objects = DesignOrderManager()

    @models.permalink
    def get_absolute_url(self):
        return ('order_detail', (self.id, ))

    def assign_designer(self, designer):
        self.designer = designer
        self.status = STATUS_ASSIGNED
        self.save()

    def complete(self, user):
        self.status = STATUS_COMPLETED
        self.completed = datetime.now()
        self.save()


class DesignOrderEvent(models.Model):
    """
    A record of a state change in a design order.
    """
    order = models.ForeignKey(DesignOrder,
        help_text=_('The order that generated this event.'))
    actor = models.ForeignKey(User, null=True, blank=True,
        help_text=_('The user that generated this event.'))
    event_type = models.CharField(_('Event Type'), max_length=10,
        help_text=_('The type of event that occurred.'))
    timestamp = models.DateTimeField(_('Arrival Timestamp'), auto_now_add=True,
        help_text=_('A timestamp of when this event was created.'))
    description = models.CharField(_('Order Source'), max_length=10, null=True, blank=True,
        help_text=_('A description of the event'))

    # TODO: catalog event types..
    #  - status change
    #    ( assigned [by, to], clarification requested, clarification provided, completed [by]
    #      accepted/rejected [rating/reason] )
    #  - note added [by]
    #  - attachment added/removed [by]


    def __unicode__(self):
        return 'DesignOrderEvent(id=%s,order=%d,user=%s,type=%s,ts=%s)' % (
                    id, order, actor, event_type, timestamp )

class CompletedDesignFile(models.Model):
    """
    Associates an order with deliverable design products. Typicall zip files containing
    """
    order = models.ForeignKey(DesignOrder, related_name='attachments',
        help_text=_('The order this design package was generated for.'))
    delivered = models.DateTimeField(_('Dispatch Timestamp'),
        default=datetime.now,
        help_text=_('The timestamp of when this package was sent to the customer.'))
    ## TODO: use s3 storage
    attachment = models.FileField(_('Completed Design File'),
        upload_to=DESIGN_UPLOAD_LOCATION, null=False,
        help_text=_('The attached design file.'))

    attachment_type = models.CharField(_('File Type'), max_length='8',
        help_text=_('The type of file attachment - e.g. KIT, PDF or ZIP'))

    def get_absolute_url(self):
        return attachment and attachment.url or 'Unbound CompletedDesignFile object'

class KitchenDesignRequest(DesignOrder):
    ### for now, a convenient way to isolate order info from order tracking info..
    ### also, tbd BathDesignRequst, ClosetDesignRequest
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

    desired = models.DateTimeField('Desired Completion', null=True, blank=True)
    submitted = models.DateTimeField(null=True, blank=True)

    tracking_notes = models.TextField(null=True, blank=True)
