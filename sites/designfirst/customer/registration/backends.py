"""
customizations of django-registration for the design service usa dealer site

this backend implements the following workflow -
 1) potential users fill out a comprehensive registration form and submit it for approval as 'registered dealers' 
     a) information from the registration form is used to create a new dealer account in 'pending' status, a primary account user, 
        and a user profile that links the user and dealer objects.
     b) a 'thank you for registering' email is sent to the primary user created for the prospective dealer.
     c) a 'new-registration' event is triggered. 
 2) site admin or customer service will recognize the new dealer, approve it, and set its status to 'active'
     a) this triggers sending of the activation email
 3) user recieves activation email, comes back to site and completes their profile by setting a real username and password
    for their account
 
"""
from datetime import datetime
from hashlib import sha1

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.sites.models import Site, RequestSite
from django.http import Http404
from django.db import transaction

from customer.models import Dealer, UserProfile
from registration.backends.default import DefaultBackend
from registration.models import RegistrationProfile, SHA1_RE
from registration.signals import user_registered

from forms import DealerRegistrationForm
from notifications import notify_new_dealer_registration

import logging

logger = logging.getLogger('customer.registration.backends')
        
class DealerRegistrationBackend(DefaultBackend):
    
    @transaction.commit_manually
    def register(self, request, **kwargs):
        """
        Given core dealer information, create a new ``Dealer`` object 
        in 'PENDING' status.

        Along with the new ``Dealer`` object, a new
        ``registration.models.RegistrationProfile`` will be created,
        tied to that ``Dealer``, containing the activation key which
        will be used for this account.

        An email will be sent to the supplied email address; this
        email should contain an activation link. The email will be
        rendered using two templates. See the documentation for
        ``RegistrationProfile.send_activation_email()`` for
        information about these templates and the contexts provided to
        them.

        After the ``Dealer`` and ``RegistrationProfile`` are created and
        the activation email is sent, the signal
        ``registration.signals.user_registered`` will be sent, with
        the new ``User`` as the keyword argument ``user`` and the
        class of this backend as the sender.

        """        
        
        logger.debug('DealerRegistrationBackend: register(%s) called', kwargs)
        
        first_name, last_name, company_name, email = kwargs.pop('first_name'), kwargs.pop('last_name'), kwargs['legal_name'], kwargs['email']
        notes = {}
        for key in ('rush', 'product_type', 'revisions', 'expected_orders', 'tos' ):
            notes[key] = kwargs.pop(key)
        
        if Site._meta.installed:
            site = Site.objects.get_current()
        else:
            site = RequestSite(request)

        temp_username = sha1(company_name+str(datetime.now())).hexdigest()[:25]
        new_user = RegistrationProfile.objects.create_inactive_user(temp_username, email,
                                                                    None, site, send_email=False)
        try:
            new_user.first_name = first_name
            new_user.last_name = last_name
            new_user.save()
            
            new_dealer = Dealer(**kwargs)
            new_dealer.notes = '\n'.join(['%s: %s' % (k,v) for (k,v) in notes.items()])
            new_dealer.status = Dealer.Const.PENDING
            new_dealer.save()
            
            new_profile = UserProfile(user=new_user, account=new_dealer)
            new_profile.primary = True
            new_profile.save()        
            
            notify_new_dealer_registration(new_dealer)
                
        except Exception as ex:
            logger.error('DealerRegistrationBackend: registration failure: %s - rolling back', ex)
            transaction.rollback()
            new_user.delete()
            transaction.commit()
#            return False
            raise ex
        else:
            transaction.commit()
        
        user_registered.send(sender=self.__class__,
                                     user=new_user,
                                     request=request)
        logger.info('DealerRegistrationBackend: new registration for %s/%s', new_user, new_dealer)
        return new_user 


#    def approve(self, request, activation_key):
#        """
#        Given an an activation key, look up and approve the dealer
#        account corresponding to that key (if possible).
#        """
#        try:
#            user = RegistrationProfile.objects.get(activation_key__exact=activation_key)
#            account = user.get_profile().account
#            if account.status == Dealer.PENDING:
#                account.approve()
#                return account
#            elif not account.status == Dealer.ACTIVE:
#                raise RuntimeError('invalid operation') 
#        except RegistrationProfile.DoesNotExist:
#            raise Http404()
#        
#        return False
#        
        
    def activate(self, request, activation_key):
        """
        Given an an activation key, look up and activate the dealer
        account corresponding to that key (if possible).
        
        Presumes the account has been approved already. If the account
        of the user is in an inactive status we throw an error.        
        """
        ## make sure user is eligible for validation
        try:
            profile = RegistrationProfile.objects.get(activation_key__exact=activation_key)
            dealer = profile.user.get_profile().account
            if dealer.status == dealer.Const.ACTIVE:                
                user = super(DealerRegistrationBackend, self).activate(request, activation_key)
                ## log the user in and redirect them to the password reset page
                internal = User.objects.make_random_password()
                user.set_password(internal)
                user.save()
                user = authenticate(username=user.username, password=internal)
                login(request, user)
                return user
            else:
                raise RuntimeError("This account can not be activated, please contact support")
            
        except RegistrationProfile.DoesNotExist:
            raise Http404()
        
        return False

    def can_activate(self, activation_key):
        if SHA1_RE.search(activation_key):
            try:
                profile = RegistrationProfile.objects.get(activation_key=activation_key)
            except RegistrationProfile.DoesNotExist:
                return False
            if not profile.activation_key_expired():
                return True
        return False

    def get_form_class(self, request):
        return DealerRegistrationForm
    
    def post_registration_redirect(self, request, user):
        """
        In addition to providing the redirect address, we also send the registration acknowledgement
        """
        
        return ('registration_complete', [], {})

    def post_activation_redirect(self, request, user):
        return ('home', [],{})

