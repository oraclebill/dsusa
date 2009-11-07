import datetime
import random
import re

from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.db import models
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.hashcompat import sha_constructor
from django.utils.translation import ugettext_lazy as _
from django.core.mail import EmailMessage
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

SHA1_RE = re.compile('^[a-f0-9]{40}$')


def make_message(subject_template, body_template, recipients, sender=None,
                                 extra_context=None, html=False, send=False):
    context = {
        'site': Site.objects.get_current(),
    }
    if extra_context:
        context.update(extra_context)

    subject = render_to_string(subject_template, context)
    # Email subject *must not* contain newlines
    subject = ''.join(subject.splitlines())

    message = render_to_string(body_template, context)
    sender = sender or settings.DEFAULT_FROM_EMAIL

    msg = EmailMessage(subject, message, sender, recipients)
    if html:
        msg.content_subtype = "html"
    if send:
        msg.send()
    else:
        return msg


class RegistrationManager(models.Manager):
    """
    Custom manager for the ``RegistrationProfile`` model.

    The methods defined here provide shortcuts for account creation
    and activation (including generation and emailing of activation
    keys), and for cleaning out expired inactive accounts.

    """

    def key_valid(self, activation_key):
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return None
            if not profile.activation_key_expired() \
                   and profile.status == 'authorized':
                return profile
        return None

    def activate(self, activation_key):
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False, False
            if not profile.activation_key_expired() \
                                and profile.status == 'authorized':
                profile.status = 'activated'
                profile.save()
                return True
        return False

    def send_activation_email(self, registration_profile, email=None):
        """
        Send email with activation code to an authorized user.
        """
        make_message(
            'registration/activation_email_subject.txt',
            'registration/activation_email.txt',
            [email or registration_profile.content_object.email],
            extra_context={
                'activation_key': registration_profile.activation_key,
                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                'profile': registration_profile,
            },
            html=getattr(settings, 'REGISTRATION_EMAIL_HTML', False),
            send=True)

    def send_registered_email(self, registration_profile, email=None):
        """
        Send email to registered but not yet authorized user.
        """
        make_message(
            'registration/registration_email_subject.txt',
            'registration/registration_email.txt',
            [email or registration_profile.content_object.email],
            extra_context={
                'profile': registration_profile,
            },
            html=getattr(settings, 'REGISTRATION_EMAIL_HTML', False),
            send=True)

    def create_profile(self, related_object):
        """
        Create a ``RegistrationProfile`` for a given
         related object, and return the ``RegistrationProfile``.

        """
        profile = self.create(content_object=related_object)
        return profile

    def authorize(self, profile):
        from registration.signals import user_authorized
        today = datetime.date.today()

        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        activation_key = sha_constructor(
            salt + str(profile.pk) + str(today)
        ).hexdigest()

        profile.status = 'authorized'
        profile.activation_key = activation_key
        profile.authorisation_date = today
        profile.save()

    def authorized(self):
        return self.filter(status='authorized')

    def unauthorized(self):
        return self.filter(status='not-authorized')


class RegistrationProfile(models.Model):
    """
    A simple profile which stores an activation key for use during
    user account registration.

    """
    STATUSES = (
        ('not-authorized', _('Not authorized')),
        ('autorized', _('Authorized')),
        ('activated', _('Activated')),
    )

    activation_key = models.CharField(_('activation key'), max_length=40, blank=True)
    authorisation_date = models.DateField(null=True)
    status = models.CharField(_('status'), choices=STATUSES, max_length=25, default='not-authorized')

    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()

    objects = RegistrationManager()

    class Meta:
        verbose_name = _('registration profile')
        verbose_name_plural = _('registration profiles')
        permissions = (
            ("can_authorize", "Can authorize users"),
        )

    def __unicode__(self):
        return u"Registration information for %s" % self.user

    def activation_key_expired(self):
        """
        Determine whether this ``RegistrationProfile``'s activation
        key has expired, returning a boolean -- ``True`` if the key
        has expired.

        """
        if not self.status == 'authorized':
            return False
            
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.authorisation_date + expiration_date <= datetime.date.today()
    activation_key_expired.boolean = True
