import logging

from django.db import models
from django.utils.translation import ugettext as _
from django.contrib.contenttypes import models as ct_models
from django.contrib.auth.models import User
import django.dispatch
from datetime import datetime


log = logging.getLogger('dsprovider.models')

DESIGN_UPLOAD_LOCATION = 'design-packages/'  ## TODO: add order id
ATTACHMENTS_LOCATION = 'order-attachments/'  ## TODO: add order id

# delivery option choices
DO_COLORVIEWS, DO_ELEVATIONS, DO_CABINETQUOTE = range(3)

# status (tbd)
STATUS_NEW, STATUS_ASSIGNED, STATUS_COMPLETED, STATUS_ACCEPTED, \
    STATUS_REJECTED, STATUS_NEW_CLARIFY, STATUS_ASSIGNED_CLARIFY = range(7)


class UserProfile(models.Model):
    """
    A profile for users that of the designer portal.
    """
    user = models.ForeignKey(User, primary_key=True, related_name='order_profile')
    is_manager = models.BooleanField(_('Special Admin Status?'), default=False)
    is_notified = models.BooleanField(_('Receive order notifications'),
                                      default=True)


def create_profile(sender, instance, **kwargs):
    UserProfile.objects.get_or_create(user=instance)

models.signals.post_save.connect(create_profile, sender=User)


class DesignOrderManager(models.Manager):

    class Meta:
        model = 'DesignOrder'

order_saved = django.dispatch.Signal(providing_args=("instance", "created"))


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

    color_views = models.BooleanField(_('Color Views'), blank=True)
    elevations = models.BooleanField(_('Elevations'), blank=True)
    quote_cabinet_list = models.BooleanField(_('Quoted Cabinet List'), default=True)
    rush = models.BooleanField(_('Same Day?'), default=False)

    final_type = models.ForeignKey(ct_models.ContentType, editable=False)

    objects = DesignOrderManager()

    def save(self, *args, **kwargs):
        self.final_type = \
                    ct_models.ContentType.objects.get_for_model(type(self))
        created = not bool(DesignOrder.objects.filter(pk=self.pk).extra(select={'a': 1}))
        super(DesignOrder, self).save(*args, **kwargs)
        order_saved.send(
            sender=DesignOrder, instance=self, created=created)

    @models.permalink
    def get_absolute_url(self):
        return ('order_detail', (self.id, ))

    def upcast(self):
        if not hasattr(self, '_upcast'):
            if isinstance(self, self.final_type.model_class()):
                self._upcast = self
            else:
                self._upcast = self.final_type.get_object_for_this_type(
                                                                    pk=self.pk)
        return self._upcast

    def assign_designer(self, designer):
        self.designer = designer
        self.status = STATUS_ASSIGNED
        self.save()

    def complete(self, user):
        self.status = STATUS_COMPLETED
        self.completed = datetime.now()
        self.save()


def order_notify(sender, instance, created, **kwargs):
    if not created:
        return

    from django.conf import settings
    from django.core import mail
    from django.contrib.sites import models as s_models
    from django.template import loader

    def make_message(subject_template, body_template, to):
        context = {
            'site': s_models.Site.objects.get_current(),
            'order': instance,
        }

        # Email subject *must not* contain newlines
        msg = mail.EmailMessage(
            subject=''.join(
                loader.render_to_string(subject_template, context).splitlines(),
            ),
            body=loader.render_to_string(body_template, context),
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=to,
        )

        msg.content_subtype = "html"  # Main content is now text/html
        return msg

    try:
        make_message(
            subject_template='designer/notification/new_order_subject.txt',
            body_template='designer/notification/new_order_body.html',
            to=User.objects.filter(order_profile__is_notified=True).values_list('email', flat=True),
        ).send()
    except Exception, e: 
        log.error('Error sending mail: %s' % e)
        
order_saved.connect(order_notify)


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

class DesignPackage(models.Model):
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
        return attachment and attachment.url or 'Unbound DesignPackage object'
    
class KitchenDesignRequest(DesignOrder):
    ### for now, a convenient way to isolate order info from order tracking info..
    ### also, tbd BathDesignRequst, ClosetDesignRequest
    # format options

    user_sketch = models.ImageField(upload_to=ATTACHMENTS_LOCATION)

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
    HW_NONE, HW_ANY, HW_HANDLE, HW_KNOB = ('NONE','ANY', 'BAR', 'KNOB')
    HW_TYPE_OPTIONS= ( (HW_NONE, _('None')), ( HW_ANY, _('Any')), ( HW_HANDLE, _('Bar Handle')), ( HW_KNOB,  _('Knob Handle')) )
    door_hardware_type      = models.CharField(_('Door Handle Type'), max_length='5', choices=HW_TYPE_OPTIONS, default=HW_ANY)
    door_hardware_model     = models.CharField(_('Door Handle Model'), max_length=20, blank=True, null=True)
    drawer_hardware_type    = models.CharField(_('Drawer Handle Type'), max_length='5', choices=HW_TYPE_OPTIONS, default=HW_ANY)
    drawer_hardware_model   = models.CharField(_('Drawer Handle Model'), max_length=20, blank=True, null=True)

    # mouldings
    ceiling_height = models.CharField(max_length=6, blank=True, null=True)
    top_moulding_1 = models.CharField(_('Top Moulding #1'), max_length=20, blank=True, null=True,
        help_text=_('Moulding along top edge of a wall cabinet - closest to ceiling'))
    top_moulding_2 = models.CharField(_('Top Moulding #2'), max_length=20, blank=True, null=True,
        help_text=_('Top of wall cabinet moulding below moulding #1'))
    top_moulding_3 = models.CharField(_('Top Moulding #3'), max_length=20, blank=True, null=True,
        help_text=_('Top of wall cabinet moulding below moulding #2'))
        
    bottom_moulding_1 = models.CharField(_('Bottom Moulding #1'), max_length=20, blank=True, null=True,
        help_text=_('Bottom of wall cabinet moulding along bottom edge of cabinet - closest to floor'))
    bottom_moulding_2 = models.CharField(_('Bottom Moulding #2'), max_length=20, blank=True, null=True,
        help_text=_('Bottom of wall cabinet moulding above moulding #1'))
    bottom_moulding_3 = models.CharField(_('Bottom Moulding #3'), max_length=20, blank=True, null=True,
        help_text=_('Bottom of wall cabinet moulding above moulding #2'))
                
    # base_moulding_1 = models.CharField(_('Base Moulding #1'), max_length=20, blank=True, null=True,
    #     help_text=_('Base cabinet moulding closest to floor.'))

    # soffits
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
    CC_ANY, CC_SQUARE, CC_DIAGONAL = ('ANY', 'SQUARE', 'DIAG')
    CORNER_CABINET_OPTIONS = ( (CC_ANY, _('Any')), (CC_SQUARE, _('Square')), (CC_DIAGONAL, _('Diagonal')) )
    CC_LEFT, CC_RIGHT = ('LEFT', 'RIGHT')
    CORNER_CABINET_OPENING_OPTIONS = ( (CC_ANY, _('Any')), (CC_LEFT, _('Left')), (CC_RIGHT, _('Right')) )   
    CC_FLAT, CC_LAZY = ('FLAT', 'LAZY')
    CORNER_CABINET_SHELVING_OPTIONS = ( (CC_ANY, _('Any')), (CC_FLAT, _('Shelf')), (CC_LAZY, _('Lazy Suzan')) )
    
    base_corner_cabinet = models.CharField(_('Base Corner Cabinets'), max_length=5, choices=CORNER_CABINET_OPTIONS, default=CC_ANY)
    base_corner_cabinet_opening = models.CharField(_('Base Corner Cabinets Opening'), max_length=5, choices=CORNER_CABINET_OPENING_OPTIONS, default=CC_ANY)
    base_corner_cabinet_shelving = models.CharField(_('Base Corner Cabinets Shelving'), max_length=15, choices=CORNER_CABINET_SHELVING_OPTIONS, default=CC_ANY)
    wall_corner_cabinet = models.CharField(_('Wall Corner Cabinets'), max_length=5, choices=CORNER_CABINET_OPTIONS, default=CC_ANY)
    wall_corner_cabinet_opening = models.CharField(_('Wall Corner Cabinets Opening'), max_length=5, choices=CORNER_CABINET_OPENING_OPTIONS, default=CC_ANY)
    wall_corner_cabinet_shelving = models.CharField(_('Wall Corner Cabinets Shelving'), max_length=15, choices=CORNER_CABINET_SHELVING_OPTIONS, default=CC_ANY)

    # TODO: island / peninsula
    island_peninsula_option = models.CharField( max_length=1, default='N',
        choices=(('N', 'None'), ('S','Single Height'), ('R', 'Raised Eating Bar')))

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
