from uuid import uuid1
from datetime import datetime
from decimal import Decimal
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models, transaction
from django.db.models import permalink
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _
from django.core.mail import mail_managers

from notification import models as notification

from signals import new_dealer_approved


logger = logging.getLogger('customer.models')

class IllegalState(Exception):
    pass

class ActiveDealerManager(models.Manager):
    def get_query_set(self):
        return super(ActiveDealerManager, self).get_query_set().filter(status__exact=Dealer.Const.ACTIVE)
        
class Dealer(models.Model):
    """
    An individual or enterprise that purchases services from DesignFirst.
    
    Customer entities are created through a registration process. Once customers
    are registered they are given the ability to create and modify new orders, and to 
    review the status of any orders that they have created. 
    """
    # class Meta:
    #     abstAract = True
    class Const:
        PENDING, ACTIVE, SUSPENDED, CANCELLED, ARCHIVED = ('P', 'A', 'S', 'C', 'R')
        ACCOUNT_STATUSES = ( 
            (PENDING, _('Pending')), (ACTIVE, _('Active')), (SUSPENDED, _('Suspended')), 
            (CANCELLED, _('Cancelled')), (ARCHIVED, _('Archived') ),
        )

    status  = models.CharField(_('Account Status'), max_length=1, choices=Const.ACCOUNT_STATUSES, default=Const.PENDING)    
    internal_name = models.SlugField(_('Account Code'), blank=True) # e.g. 'dds-010-...'
    legal_name = models.CharField(_('Business Name'), max_length=50, unique=True)
    address_1 = models.CharField(_('Address 1'), max_length=40, blank=True, null=True)
    address_2 = models.CharField(_('Address 2'), max_length=40, blank=True, null=True)
    city = models.CharField(_('City'), max_length=20, blank=True, null=True)
    state = models.CharField(_('State'), max_length=2, blank=True, null=True)
    zip4 = models.CharField(_('Zip Code'), max_length=10, blank=True, null=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    fax = models.CharField(_('Fax'), max_length=20, blank=True)
    email = models.EmailField(_('Email'), blank=True)
    
    account_rep_name = models.CharField(_('Account Rep Name'), max_length=30, blank=True, null=True)
    account_rep = models.ForeignKey(User, blank=True, null=True, editable=False, related_name='rep_for_dealers', verbose_name=_('Account Rep'))
    num_locations = models.IntegerField(_('Number of Locations'), default=1)
    notes = models.TextField(_("Notes"), max_length=200, blank=True, null=True)
            
    credit_balance = models.DecimalField(_('Account Credit'), max_digits=10, decimal_places=2, default=0)

    class Meta:
        verbose_name = _('dealer')
        verbose_name_plural = _('dealers')
        
    def send_welcome(self):
        logger.debug('Dealer::send_welcome: welcoming %s', self)
        registration_key = self.primary_contact.registrationprofile_set.all()[0].activation_key
        path = reverse('registration_activate', kwargs={'activation_key': registration_key })
        protocol = settings.SECURE and 'https' or 'http'
        host = Site.objects.get_current().domain
        setup_url = '%s://%s%s' % (protocol, host, path)
        recipients = [self.primary_contact]
        if settings.ADMINS:
            admin_users = User.objects.filter(email__in=[b for (a,b) in settings.ADMINS])
            if not admin_users:
                logger.warning('send_welcome: admin_users falling back to superusers (no admins or admins emails are not system users).')
                admin_users = User.objects.filter(is_superuser=True)
            if not admin_users:
                logger.error('send_welcome: cannot find admin_user to send mail notification to.')
            recipients.extend(admin_users)
        notification.send(recipients, 'new_dealer_welcome',
            extra_context={
                'setup_url': setup_url,
                'account': self,
            }
        )
        logger.debug('send_welcome: welcome notification sent to %s.' % recipients)

    def activate(self):
        logger.info('Dealer::activate: activating %s (%s)', self, self.get_status_display())
        if self.status in ( self.Const.PENDING, self.Const.SUSPENDED, self.Const.CANCELLED ):
            self.status = self.Const.ACTIVE
            self.save()
    
    def approve(self):
        self.activate()        
        try:
            mail_managers('dealer approved - %s' % self.legal_name, 'approved')
            self.send_welcome()
        except Exception , err:
            logger.error('Dealer::approve: "%s" error sending approval mails for "%s"', err, self)
        
    def __unicode__(self):
        return self.legal_name
        
    def _primary_contact(self):
        """Return the primary contact or None."""
        try:
            return self.userprofile_set.get(primary=True).user
        except UserProfile.DoesNotExist:
            return None
            
    primary_contact = property(_primary_contact)

class UserProfile(models.Model):
    """
    Site profile associating this user with a dealer account and serving as a hook for site preferences.
    
    """    
    user = models.ForeignKey(User, unique=True, primary_key=True)
    account = models.ForeignKey(Dealer)
    primary = models.BooleanField(_('Primary Contact?'))

    class Meta:
        verbose_name = _("user profile")
        verbose_name_plural = _("user profiles")

    def save(self, force_insert=False, force_update=False):
        """
        If this user is the primary, then make sure that it is the only
        primary contact for the account. If there is no existing default, then make
        this user is the default.
        """
        existing_primary = self.account.primary_contact
        if existing_primary:
            if self.primary:
                existing_primary.primary = False
                super(UserProfile, existing_primary).save()
        else:
            self.primary = True
        super(UserProfile, self).save(force_insert=force_insert, force_update=force_update)
    
    # for profiles module
    def get_absolute_url(self):
        return ('profiles_profile_detail', (), { 'username': self.user.username })
    get_absolute_url = models.permalink(get_absolute_url)
        
    def __unicode__(self):
        if hasattr(self,'user') and hasattr(self, 'account'):
            return '%s [%s]' % (self.user.username, self.account.legal_name) 
        else:
            return '[empty user profile]'
            

def uuid_key():
    return uuid1().hex
        
class Invoice(models.Model):
    class Const:
        NEW, CANCELLED, PENDING, PAID = ('N', 'C', 'E', 'A')
        INV_STATUS_CHOICES = ((NEW, _('NEW')), (PENDING, _('PENDING')), (PAID, _('PAID')), (CANCELLED, _('FAILED')))

    id          = models.CharField(max_length=50, primary_key=True, default=uuid_key)
    customer    = models.ForeignKey(Dealer)
    status      = models.CharField(max_length=1, choices=Const.INV_STATUS_CHOICES)
    description = models.TextField(blank=True)
    created     = models.DateTimeField(auto_now_add=True)
    ## TODO
    # updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['customer', 'created',] 
        verbose_name = _('invoice')
        verbose_name_plural = _('invoices')
        
    @property
    def total(self):
        return reduce(
            lambda x,y: x+y, 
            [il.line_price for il in self.lines.all()], 
            Decimal() )
    
    @property
    def total_credit(self):
        return reduce(
            lambda x,y: x+y, 
            [il.line_credit for il in self.lines.all()], 
            Decimal() )
    
    def add_line(self, description, price, quantity=1):
        return self.lines.create(
            description=description, 
            unit_price=price, 
            quantity=quantity
        )

    def get_absolute_url(self):
        return ('invoice-detail', [], {'object_id': self.id})
    get_absolute_url = models.permalink(get_absolute_url)
        
    def __unicode__(self):
        return 'Invoice[id=%s,customer=%s,status=%s,created=%s]' % (
                    self.id or 'None', 
                    self.customer or 'None', 
                    self.status or 'None', 
                    self.created or 'None')

    
        
class InvoiceLine(models.Model):
    invoice     = models.ForeignKey(Invoice, related_name='lines')
    number      = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=80)
    quantity    = models.IntegerField()
    unit_price  = models.DecimalField(max_digits=10, decimal_places=2)
    _unit_credit  = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    class Meta:
        verbose_name = _('invoice line')
        verbose_name_plural = _('invoice lines')
        
    @property
    def unit_credit(self):
        return self._unit_credit or self.unit_price

    @property
    def line_price(self):
        return self.unit_price * self.quantity        
        
    @property
    def line_credit(self):
        return self.unit_credit * self.quantity        
    
@transaction.commit_on_success
def create_basic_dealer_account(dealer_name, username, email, account_status=Dealer.Const.PENDING, initial_balance=0, password=None, company_mail=None):
    """
    Create a skeletal Dealer, User and UserProfile.
    """
    user = User.objects.create_user(username, email, password)
    company = Dealer.objects.create(
                legal_name=dealer_name,
                status=account_status,
                email=company_mail or email,
                credit_balance=initial_balance
    )
    profile = UserProfile.objects.create(
                user = user,
                account = company,
                primary = True
    )
    return user


