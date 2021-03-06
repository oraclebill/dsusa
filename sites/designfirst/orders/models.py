from datetime import datetime, timedelta
import os.path, random, string, logging

#from django.conf import settings
from django.contrib.auth.models import User
#from django.utils.text import get_valid_filename
#from django.core.files.base import File as DjangoFile
from django.core import exceptions
from django.db.transaction import commit_on_success
from django.db import models
from django.utils.datastructures import SortedDict
from django.utils.translation import ugettext_lazy as _

from utils.pdf import pdf2ppm
from utils.fields import DimensionField
from utils.storage import AppStorage
from signals import status_changed

logger = logging.getLogger('orders.models')

LETTERS_AND_DIGITS = string.letters + string.digits
APPSTORAGE = AppStorage()        
    
def attachment_upload_location(attachment_obj, filename):
    return os.path.join( 'account-data',
        str(attachment_obj.order.owner.get_profile().account.id), 
        'order-data',
        str(attachment_obj.order.id), 
        'diagrams',
        str(filename)
    )    
    
def preview_upload_location(preview_obj, filename):
    return os.path.join( 'account-data', 
        str(preview_obj.attachment.order.owner.get_profile().account.id), 
        'order-data',
        str(preview_obj.attachment.order.id), 
        'pages',
        str(filename)
    )

def package_upload_location(package_or_file_obj, filename):
    return os.path.join( 'account-data', 
        str(package_or_file_obj.attachment.order.owner.get_profile().account.id), 
        'order-data',
        str(package_or_file_obj.attachment.order.id), 
        'designs',
        str(filename)
    )


def _get_customer_code(user):
    try:
        profile = user.get_profile()            
        if profile.account and profile.account.internal_name:
            return profile.account.internal_name
        elif profile.account:
            return profile.account.legal_name
    except:            
        return user.username 

def _generate_tracking_code(order):
    return "".join([random.choice(LETTERS_AND_DIGITS) for x in xrange(15)])

class BaseOrderManager(models.Manager):
            
    def create_order(self, owner, project_name, project_type=None, account_code=None, tracking_code=None, save=True):
        "create a new order initializing required fields"        
        order = self.model(owner=owner, project_name=project_name)
        order.project_type = project_type or order.Const.KITCHEN_DESIGN
        order.tracking_code = tracking_code or _generate_tracking_code(order)
        order.account_code = account_code or _get_customer_code(owner)
        if save:
            order.save()
        return order
                              
class BaseOrder(models.Model):
    """
    This is a temporary object used for storing data 
    when  user goes step to step in orders
    """
    class Const:
        #Basic stuff
        DEALER_EDIT, SUBMITTED, ASSIGNED, COMPLETED = range(1,5) #TODO: change from number to code
        STATUS_CHOICES = (
            (DEALER_EDIT, 'Dealer Editing'),
            (SUBMITTED, 'Submitted'),
            (ASSIGNED, 'Assigned'),
            (COMPLETED, 'Completed'),
        )
        
        KITCHEN_DESIGN, BATH_DESIGN, CLOSET_DESIGN, GENERAL_DESIGN = ('K', 'B', 'C', '*')  #TODO: change from number to code
        PROJECT_TYPE_CHOICES = (
            (KITCHEN_DESIGN, _('Kitchen')),
            (BATH_DESIGN, _('Bath')),
            (CLOSET_DESIGN, _('Closet')),
            (GENERAL_DESIGN, _('Other (Generic)')),
        )
        
    owner = models.ForeignKey(User)
#    creator = models.ForeignKey(User, related_name='orders_created')   # will replace 'owner'..
#    account = models.ForeignKey(Dealer)    
    status = models.PositiveSmallIntegerField(_('Status'), choices=Const.STATUS_CHOICES, default=Const.DEALER_EDIT)

    #whj:  new fields 11/18/09 to support tracking and fax correlation
    account_code = models.CharField(_('Customer Account Code'), max_length=40)
    tracking_code = models.CharField(_('Tracking Code'), max_length=20, null=True, blank=True)
    project_name = models.CharField(_('Project Name'), max_length=150)
    project_type = models.CharField(_('Project Type'), max_length=1, choices=Const.PROJECT_TYPE_CHOICES, default=Const.KITCHEN_DESIGN)
    created = models.DateTimeField(_('Created On'), auto_now_add=True, editable=False)
    submitted = models.DateTimeField(_('Submitted On'), null=True, blank=True, editable=False)
    completed = models.DateTimeField(_('Completed On'), null=True, blank=True, editable=False)
    
    #Submit options
    rush = models.BooleanField(_('Rush Processing'), default=False)  ## TODO: processing_options = 'NONE', 'RUSH'
    #product_selection = models.TextField(_('DSUSA Product'), null=True, blank=True)
    
    color_views = models.BooleanField(_('Include Color Perspectives'), default=False)
    elevations = models.BooleanField(_('Include Elevations'), default=False)
    quoted_cabinet_list = models.BooleanField(_('Include Cabinetry Quote'), default=False)
    desired = models.DateTimeField('Desired Delivered Date', null=True, blank=True)
    cost = models.DecimalField(_('Total Design Cost'), max_digits=10, decimal_places=2, blank=True, null=True)
    client_notes = models.TextField('Notes for the Designer', null=True, blank=True)
    finished_steps = models.CharField(max_length=250, editable=False, default='')
    updated = models.DateTimeField(_('Last Updated'), auto_now=True, editable=False)

    objects = BaseOrderManager()

    class Meta:
        abstract = True
        verbose_name = 'order'
        verbose_name_plural = 'orders'
#        unique_together = (('owner', 'project_name'),)  # TODO: integrity *does* matter..        

    def is_step_finished(self, name):
        return name in self.finished_steps

    def finish_step(self, name, commit=True):
        if not name in self.finished_steps:
            if self.finished_steps:
                self.finished_steps += ','
            self.finished_steps += name
            if commit:
                self.save()

#    @property
#    def expected(self):
#        "Expected completion time"
#        if self.submitted:
#            if self.rush:
#                delta = timedelta(days=1)
#            else:
#                delta = timedelta(days=2)
#            return self.submitted + delta
#        return None
            
    @property
    def flags(self):
        "Processing flags"
        flags = []
        if self.color_views:
            flags.append('PRSNTR')
        else:
            flags.append('PRO')            
        if self.rush:
            flags.append('RUSH')
        return ', '.join(flags)

    def save(self, force_insert=False, force_update=False):
#        if not self.project_name:
#            raise exceptions.ValidationError('All orders must contain a project name')
#        if not self.account_code:
#            raise exceptions.ValidationError('All orders must contain an account code')
#        if not (self.status and self.status in [first for (first,second) in self.Const.STATUS_CHOICES]):
#            raise ValueError('All orders must have a valid status')
        changed, old_status = self._check_status_change()

        if changed:
            if self.status == BaseOrder.Const.SUBMITTED:
                self.submitted = datetime.now()
            elif self.status == BaseOrder.Const.COMPLETED:
                self.completed = datetime.now()
                
        if self.status == self.Const.DEALER_EDIT or changed: 
            super(BaseOrder,self).save(force_insert, force_update)
            if None == old_status: # new order
                self._init_tracking_fields()
            if changed:
                status_changed.send(self, old=old_status, new=self.status)
        else:
            raise ValueError('Cannot modify order in %s status.' % self.status)
         
    def _check_status_change(self):
        if not self.id:
            return True, None        
        changed = False
        old_status = None
        new_status = self.status
        try:
            old_status = self.__class__._default_manager.get(pk=self.id).status
            changed = new_status != old_status
        except self.DoesNotExist:
            changed = True                
        return (changed, old_status)
        
    def _init_tracking_fields(self):
        if self.owner and not self.account_code:            
            self.customer_code = _get_customer_code(self.owner) 
        if not self.tracking_code:
            self.tracking_code = _generate_tracking_code(self) # get_valid_filename('%s-%02d' % (self.customer_code, self.project_name))
        
        
    def __unicode__(self):
        return self.project_name



class WorkingOrder(BaseOrder):
    
#    PAINT, STAIN, NATURAL, GLAZE = ('P', 'S', 'N', 'G')
#    FINISH_CHOICES = (
#        (STAIN, 'Stain'), (PAINT, 'Paint'), (NATURAL, 'Natural'), (GLAZE, 'Glaze'),
#    )
#
#    MAPLE, CHERRY, ALDER, LYPTUS, BIRCH, MDF, STAINLESS, PERMAFOIL, GLASS = (
#        'MAPL', 'CHER', 'ALDR', 'LYPT', 'BIRC', 'MDF', 'STEEL', 'FOIL', 'GLASS')        
#    DOOR_MATERIAL_CHOICES = ( 
#        (MAPLE, 'Maple'), (CHERRY, 'Cherry'), (ALDER, 'Alder'), (LYPTUS, 'Lyptus'), 
#        (BIRCH, 'Birch'), (MDF, 'MDF'), (STAINLESS, 'Stainless Steel'), (PERMAFOIL, 'Permafoil'), 
#        (GLASS, 'Glass'),
#    )
    
    #Manufacturer page (cabinetry options)
    manufacturer    = models.CharField(_('Manufacturer'), max_length=50, blank=True, null=True)
    product_line    = models.CharField(_('Product Line'), max_length=50, blank=True, null=True)
    door_style      = models.CharField(_('Door Style'), max_length=50, blank=True, null=True)
    drawer_front_style = models.CharField(_('Drawer Front Style'), max_length=50, blank=True, null=True)
    
    cabinet_material= models.CharField(_('Door Material'), max_length=20, blank=True, null=True)
    finish_type     = models.CharField(_('Finish Type'), max_length=50, blank=True, null=True)

    finish_color    = models.CharField(_('Paint/Stain Color'), max_length=50, blank=True, null=True) # maybe 'color'?
    finish_options  =  models.CharField(_('Finish Options'), max_length=50, blank=True, null=True)
    
        
    #Hardware page
    HANDLE_NONE, HANDLE_PULL, HANDLE_KNOB = range(3)
    HANDLE_TYPES = (
            (HANDLE_NONE, 'None / Not Specified'),
            (HANDLE_PULL, 'Pull'),
            (HANDLE_KNOB, 'Knob'))
    
    door_handle_type = models.PositiveSmallIntegerField(_('Door Handle Type'), choices=HANDLE_TYPES, default=HANDLE_NONE)
    door_handle_model = models.CharField(_('Door Handle Product'), max_length=100, null=True, blank=True)
    
    drawer_handle_type = models.PositiveSmallIntegerField(_('Drawer Handle Type'), choices=HANDLE_TYPES, default=HANDLE_NONE)
    drawer_handle_model = models.CharField(_('Drawer Handle Product'), max_length=100, null=True, blank=True)
    
    #Soffits page
    has_soffits = models.BooleanField(_('Has Soffits?'), blank=True, default=False)
    soffit_width = DimensionField(_('Width'), null=True, blank=True)
    soffit_height = DimensionField(_('Height'), null=True, blank=True)
    soffit_depth = DimensionField(_('Depth'), null=True, blank=True)
    
    
    #Dimension page
    S_NONE, S_STACKED, S_STG_HWC, S_STG_HWD, S_STG_DHWC, S_STG_HBC, S_STG_DBC = range(7)
    STYLE_CHOICES = (
        (S_NONE, _('Normal')),
        (S_STACKED, _('Stacked Wall Cabinets')),
        (S_STG_HWC, _('Staggered Depth Wall Cabinets')),
        (S_STG_DHWC, _('Staggered Depth and Height Wall Cabinets')),
        (S_STG_HBC, _('Staggered Height Base Cabinets')),
        (S_STG_DBC, _('Staggered Depth Base Cabinets')))

    STANDARD_SIZES = [12,15,18,21,24,27,30,36,42]
    dimension_style = models.PositiveSmallIntegerField(_('Cabinet Arrangements'), choices=STYLE_CHOICES, default=S_NONE)
    standard_sizes = models.BooleanField(_('Use Standard Sizes'))   
    wall_cabinet_height = DimensionField(_('Wall Cabinet Height'), null=True, blank=True)
    wall_cabinet_depth = DimensionField(_('Wall Cabinet Height'), null=True, blank=True)
    base_cabinet_height = DimensionField(_('Vanity Cabinet Height'), null=True, blank=True)
    base_cabinet_depth = DimensionField(_('Depth'), null=True, blank=True)
    vanity_cabinet_height = DimensionField(_('Vanity Cabinet Height'), null=True, blank=True)
    vanity_cabinet_depth = DimensionField(_('Depth'), null=True, blank=True)
    
    #Corder cabinet page
    CORNER_NONE, CORNER_RIGHT, CORNER_LEFT = range(3)
    BUILD_CORNER_CHOICES = (
            (CORNER_NONE, _('None')),
            (CORNER_RIGHT, _('Right Hinged')),
            (CORNER_LEFT, _('Left Hinged')))
    
    SHELF, LAZY_SUSAN = range(1,3)
    SHELVING_CHOICES = (
            (SHELF, _('Shelves')),
            (LAZY_SUSAN, _('Lazy Susan')))
    diagonal_corner_wall = models.PositiveSmallIntegerField(_('Diagonal Corner Wall'), choices=BUILD_CORNER_CHOICES, default=CORNER_NONE)
    diagonal_corner_wall_shelv = models.PositiveSmallIntegerField(_('Shelving Option'), choices=SHELVING_CHOICES, default=SHELF)
    diagonal_corner_base = models.PositiveSmallIntegerField(_('Diagonal Corner Base'), choices=BUILD_CORNER_CHOICES, default=CORNER_NONE)
    diagonal_corner_base_shelv = models.PositiveSmallIntegerField(_('Shelving Option'), choices=SHELVING_CHOICES, default=SHELF)
    degree90_corner_wall = models.PositiveSmallIntegerField(_('Ninety Degree Corner Wall'), choices=BUILD_CORNER_CHOICES, default=CORNER_NONE)
    degree90_corner_base = models.PositiveSmallIntegerField(_('Ninety Degree Corner Base'), choices=BUILD_CORNER_CHOICES, default=CORNER_NONE)
    degree90_corner_base_shelv = models.PositiveSmallIntegerField(_('Shelving Option'), choices=SHELVING_CHOICES, default=SHELF)
    
    #Interiors page
    slide_out_trays = models.CharField(_('Slide Out Trays'), max_length=15, blank=True)
    waste_bin = models.CharField(_('Waste Bin'), max_length=15, blank=True)
    wine_rack = models.CharField(_('Wine Rack'), max_length=15, blank=True)
    plate_rack = models.CharField(_('Plate Rack'), max_length=15, blank=True)
    appliance_garage = models.CharField(_('Appliance Garage'), max_length=15, blank=True)
    
    #Miscellaneous page
    corbels = models.BooleanField(_('Corbels') )
    brackets = models.BooleanField(_('Brackets') )
    valance = models.BooleanField(_('Valence') )
    legs_feet = models.BooleanField('Legs/Feet')
    glass_doors = models.BooleanField(_('Glass Doors'), )
    range_hood = models.BooleanField(_('Range Hood'), )
    posts = models.BooleanField(_('Posts'), )
    
    
    def attachment_previews(self):
        "Return urls of all attachment pages"
        return [a.preview for a in self.attachments.all()]
    
    def is_complete(self):
        return self.attachments.filter(type=Attachment.Const.FLOORPLAN)
    

class OrderDependentModel(models.Model):
    """
    Encapsulates some behaviour common to entities that are attributes of an order.
    """
    class Meta:
        abstract = True
        
    def save(self, force_insert=False, force_update=False):
        if self.order and self.order.status == BaseOrder.Const.DEALER_EDIT:
            super(OrderDependentModel,self).save(force_insert, force_update)
        elif not self.order:
            super(OrderDependentModel,self).save(force_insert, force_update)
        else:
            raise ValueError('Cannot modify order in %s status.' % self.order.status)
        
class Moulding(OrderDependentModel):
    TOP, BOTTOM, BASE, SCRIBE, OTHER = range(1,6)
    TYPE_CHOICES = (
        (TOP, _('Top of Wall Cabinet')),
        (BOTTOM, _('Bottom of Wall Cabinet')),
        (BASE, _('Base Cabinet')),
        (SCRIBE, _('Scribe')),
        (OTHER, _('Other')),
    )
    order = models.ForeignKey(WorkingOrder, related_name='mouldings')
    num = models.PositiveIntegerField(_('#'),)
    type = models.PositiveSmallIntegerField(_('Type'), choices=TYPE_CHOICES)
    name = models.CharField(_('Moulding Style/Model'), max_length=255)
    
    class Meta:
        ordering = ['order', 'type', 'num']
    
    def __unicode__(self):
        return '#%s %s %s' % (self.num, self.get_type_display(), self.name)
    
    def save(self, *args, **kwargs):
        if self.num is None:
            self.num = self._next_num()
        super(Moulding, self).save(*args, **kwargs)
    
    def delete(self):
        order, type = self.order, self.type
        super(Moulding, self).delete()
        self.reorder(order, type)
    
    def _next_num(self):
        items = list(Moulding.objects.filter(order=self.order, type=self.type))
        if len(items) == 0:
            return 1
        return items[-1].num + 1
    
    @classmethod
    def groups(cls, order):
        "Returns mouldings grouped by type"
        data = SortedDict()
        items = list(cls.objects.filter(order=order))
        for t,n in cls.TYPE_CHOICES:
            type_items = [i for i in items if i.type == t]
            if len(type_items) > 0:
                data[n] = type_items 
        return data
    
    @classmethod
    @commit_on_success
    def reorder(cls, order, type, new_sort_order=None):
        if new_sort_order is None:
            items = cls.objects.filter(order=order, type=type)
        else:
            items = [cls.objects.get(order=order, type=type, pk=i) for i in new_sort_order]
        i = 1
        for item in items:
            item.num = i
            item.save()
            i += 1
                

class RequestNotation(OrderDependentModel):
    """
    A notation provided by the requestor, specifying or clarifying something in a way that is not 
    otherwise possible in the interface.
    
    Notations may also be captured from notes in submitted diagrams.
    """
    author      = models.ForeignKey(User, 
                                    related_name='order_notes', 
                                    verbose_name=_("author"),
                                    help_text=_("The user that created this notation."))
    order       = models.ForeignKey(WorkingOrder, 
                                    related_name='notes',
                                    verbose_name=_("design request"),
                                    help_text=_("The design request this notation refers to."))
    note_text   = models.TextField(_("note text"),
                                   help_text=_("The content of the notation"))
    created         = models.DateTimeField(_("created"), 
                                           auto_now_add=True,
                                           help_text=_("Timestamp of this notes creation."))
    area_reference  = models.CharField(_("referenced area"), 
                                       max_length=50, 
                                       null=True, 
                                       blank=True,
                                       help_text=_("The area (within the wizard or data entry application) that\
                                       this comment was captured in. This is an optional item."))
    field_reference = models.CharField(_("referenced field"), 
                                       max_length=50, 
                                       null=True, 
                                       blank=True,
                                       help_text=_("The name of the field this comment or notation applies to. This \
                                       is an optional item."))
    
    class Meta:
        unique_together = ('order', 'area_reference', 'field_reference', )
        
    def save(self, *args, **kwargs):
        if not self.order.status == BaseOrder.Const.DEALER_EDIT:
            raise ValueError('Cannot modify notes associated with order in %s status' % self.order.status ) 
        super(RequestNotation, self).save(*args, **kwargs)


class Attachment(OrderDependentModel):
    class Const:
        FLOORPLAN, PHOTO, OTHER = range(1,4)
        TYPE_CHOICES = (
                (FLOORPLAN, _('Floorplan Sketch')),
                (PHOTO, _('Photograph')),
                (OTHER, _('Other')),)
        UPLOADED, FAXED = ('U','F')
        ATTACHMENT_SRC_CHOICES=((UPLOADED, _('Uploaded')),(FAXED, _('Faxed')),)
    
    order = models.ForeignKey(WorkingOrder, related_name='attachments')
    type = models.PositiveSmallIntegerField(_('type'), choices=Const.TYPE_CHOICES, default=Const.FLOORPLAN)
    file = models.FileField(_('file'), upload_to=attachment_upload_location, storage=APPSTORAGE)
    source = models.CharField(_('attachment method'), max_length=1, choices=Const.ATTACHMENT_SRC_CHOICES, default=Const.UPLOADED, editable=False)
    timestamp = models.DateTimeField(_('uploaded on'), auto_now_add=True)
    page_count = models.PositiveSmallIntegerField(_('page count'), default=1)

    class Meta:
        verbose_name = _('attachment')
        verbose_name_plural = _('attachments')
        ordering = ['-order', '-timestamp']
    
    def __unicode__(self):
        return self.file and os.path.basename(self.file.path) or '(no file)'

    @property
    def preview(self):
        if self.page_count > 1:
            return self.attachmentpage_set.all()[0].file
        return self.file 
    
    @property
    def pages(self):
        if self.page_count > 1:
            for f in self.attachmentpage_set.all():
                yield {'file':f.file, 'page': f.page}
        else:
            yield {'file':self.file, 'page': 1}
                
    def split_pages(self):
        if self.file.name.lower().endswith('.pdf'):
            self.attachmentpage_set.all().delete()
            try:
                self.page_count = pdf2ppm(self.file.path, self._pdf_callback)
                self.save()
            except OSError as ex:
                logger.error('%s error during page generation for %s' % (ex, self))
    
    def _pdf_callback(self, image, name, page):
        logger.debug('enter: _pdf_callback(%s, %s, %s, %s)' % (self, image, name, page))
        page_obj = self.attachmentpage_set.create(page=page, 
                                file=attachment_upload_location(self, "%s-page-%d.png" % (name, page)),
                                thumb=attachment_upload_location(self, "%s-page-%d-thumb.png" % (name, page)))
        try:
            file = open(page_obj.file.path, 'wb')
            image.copy().save(file)
            file.close()
            file = open(page_obj.thumb.path, 'wb')
            image.thumbnail((50,70))
            image.save(file)
            file.close()
        except Exception as ex:
            logger.error('_pdf_callback (%s): %s' % (self, ex))
        else:
            page_obj.save()        


class AttachmentPage(models.Model):
    "Stores PDF pages converted to images"
    attachment = models.ForeignKey(Attachment)
    page = models.PositiveIntegerField(_('page number'), )
    file = models.ImageField(_('page'), max_length=180, upload_to=preview_upload_location, storage=APPSTORAGE)
    thumb = models.ImageField(_('thumbnail'), max_length=180, upload_to=preview_upload_location, storage=APPSTORAGE, null=True)
    
    class Meta:
        verbose_name = _('attachment preview')
        verbose_name_plural = _('attachment pages')
        ordering = ['attachment', 'page']
    
    def __unicode__(self):
        return '%s#%d' % (self.attachment, self.page)
    

class Appliance(OrderDependentModel):
    TYPES = ['Bar Sink',
             'Coffee Maker',
             'Cooktop',
             'Dishwasher',
             'Double Oven',
             'Double sink',
             'Microwave',
             'Offset Sink',
             'Oven',
             'Range',
             'Range Top',
             'Refrigerator',
             'Sink',
             'Under Counter Refrigerator',
             'Vent Hood'
            ]
    
    order = models.ForeignKey(WorkingOrder, editable=False, related_name='appliances')
    type = models.CharField(_('Type'), max_length=20, choices=[(i,i) for i in TYPES])
    model = models.CharField(_('Model'), max_length=30, null=True, blank=True)
    width = DimensionField(_('Width'), null=True, blank=True)
    height = DimensionField(_('Height'), null=True, blank=True)
    depth = DimensionField(_('Depth'), null=True, blank=True)
    options = models.CharField(_('Options'), max_length=80, null=True, blank=True)
    
    def __unicode__(self):
        return self.type


class DesignPackage(models.Model):
    """
    Associates an order with deliverable design products.
    
    Design packages contain at least a .KIT file, and possibly a price report 
    and a collection of images - floorplans, elevations and perspective views
    """
    order = models.ForeignKey(WorkingOrder, related_name='designpackage',
        help_text=_('The order this design package was generated for.'))
    #version = models.IntegerField('Revision Number', unique=True)
    created = models.DateTimeField(_('Created'),
        default=datetime.now, help_text=_('The timestamp of when this package was sent to the customer.'))


class DesignPackageFile(models.Model):
    '''
    A file in design package delivered to a customer.
    '''
    class Const:
        KIT, QUOTE, ARCHIVE, PERSPECTIVE, FLOORPLAN, ELEVATION= 'K', 'Q', 'A', 'P', 'F', 'E'  
        DP_ATTACHMENT_CHOICES = ((KIT, '20/20 KIT File'), 
                                 (QUOTE, 'Quote'), 
                                 (ARCHIVE, 'Image Archive'), 
                                 (PERSPECTIVE, 'Image File'),
                                 (FLOORPLAN, 'Image File'),
                                 (ELEVATION, 'Image File'),
        )
    design_package = models.ForeignKey(DesignPackage)
    type = models.CharField(_('type'), max_length=1, choices=Const.DP_ATTACHMENT_CHOICES)
    file = models.FileField(_('file'), upload_to=package_upload_location, storage=APPSTORAGE)
    
