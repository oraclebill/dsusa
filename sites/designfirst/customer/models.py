from uuid import uuid1
from datetime import datetime
from decimal import Decimal

from django.conf import settings
from django.db import models, transaction
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.utils.translation import ugettext, ugettext_lazy as _


class IllegalState(Exception):
    pass


class Dealer(models.Model):
    """
    An individual or enterprise that purchases services from DesignFirst.
    
    Customer entities are created through a registration process. Once customers
    are registered they are given the ability to create and modify new orders, and to 
    review the status of any orders that they have created. 
    """
    # class Meta:
    #     abstAract = True
    PENDING, ACTIVE, SUSPENDED, CANCELLED, ARCHIVED = ('P', 'A', 'S', 'C', 'R')
    ACCOUNT_STATUSES = ( 
        (PENDING, _('Pending')), (ACTIVE, _('Active')), (SUSPENDED, _('Suspended')), 
        (CANCELLED, _('Cancelled')), (ARCHIVED, _('Archived') ),
    )
    status  = models.CharField(_('Account Status'), max_length=1, choices=ACCOUNT_STATUSES, default=PENDING)    
    internal_name = models.SlugField(_('Account Code')) # e.g. 'dds-010-...'
    legal_name = models.CharField(_('Business Name'), max_length=50)
    address_1 = models.CharField(_('Address 1'), max_length=40, blank=True, null=True)
    address_2 = models.CharField(_('Address 2'), max_length=40, blank=True, null=True)
    city = models.CharField(_('City'), max_length=20, blank=True, null=True)
    state = models.CharField(_('State'), max_length=2, blank=True, null=True)
    zip4 = models.CharField(_('Zip Code'), max_length=10, blank=True, null=True)
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    fax = models.CharField(_('Fax'), max_length=20, blank=True)
    email = models.EmailField(_('EMail'), blank=True)
    
    account_rep_name = models.CharField(_('Account Rep Name'), max_length=30, blank=True, null=True)
    account_rep = models.ForeignKey(User, blank=True, null=True, editable=False, related_name='rep_for_dealers', verbose_name=_('Account Rep'))
    num_locations = models.IntegerField(_('Number of Locations'), default=1)
    notes = models.TextField(_("Notes"), max_length=200, blank=True, null=True)
            
    credit_balance = models.DecimalField(_('Account Credit'), max_digits=10, decimal_places=2, default=0)
    
    def __unicode__(self):
        return self.legal_name
        
    def _primary_contact(self):
        """Return the primary contact or None."""
        try:
            return self.userprofile_set.get(primary=True)
        except UserProfile.DoesNotExist:
            return None
    primary_contact = property(_primary_contact)
        
class UserProfile(models.Model):
    """
    Site profile associating this user with either a customer account or designer profile.
    
    """    
    user = models.ForeignKey(User, primary_key=True, unique=True)
    account = models.ForeignKey(Dealer)
    primary = models.BooleanField(_('Primary Contact?'))

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
            return '%s @ %s' % (self.user, self.account) 
        else:
            return '[empty user profile]'
            
    class Meta:
        verbose_name = _("User Profile")
        verbose_name_plural = _("User Profiles")

def uuid_key():
    return uuid1().hex
        
class Invoice(models.Model):
    NEW, CANCELLED, PENDING, PAID = ('N', 'C', 'E', 'A')
    INV_STATUS_CHOICES = ((NEW, _('NEW')), (PENDING, _('PENDING')), (PAID, _('PAID')), (CANCELLED, _('CANCELLED')))

    id          = models.CharField(max_length=50, primary_key=True, default=uuid_key)
    customer    = models.ForeignKey(Dealer)
    status      = models.CharField(max_length=1, choices=INV_STATUS_CHOICES)
    description = models.TextField(blank=True)
    created     = models.DateTimeField(auto_now_add=True)
    ## TODO
    # updated = models.DateTimeField(auto_now=True)
    
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
    
    @property
    def unit_credit(self):
        return self._unit_credit or self.unit_price

    @property
    def line_price(self):
        return self.unit_price * self.quantity        
        
    @property
    def line_credit(self):
        return self.unit_credit * self.quantity        
        
