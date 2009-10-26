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
    def activate_user(self, activation_key):
        """
        Validate an activation key and activate the corresponding
        ``User`` if valid.

        If the key is valid and has not expired, return the ``User``
        after activating.

        If the key is not valid or has expired, return ``False``.

        If the key is valid but the ``User`` is already active,
        return ``False``.

        To prevent reactivation of an account which has been
        deactivated by site administrators, the activation key is
        reset to the string constant ``RegistrationProfile.ACTIVATED``
        after successful activation.

        To execute customized logic when a ``User`` is activated,
        connect a function to the signal
        ``registration.signals.user_activated``; this signal will be
        sent (with the ``User`` as the value of the keyword argument
        ``user``) after a successful activation.

        """
        from registration.signals import user_activated

        # Make sure the key we're trying conforms to the pattern of a
        # SHA1 hash; if it doesn't, no point trying to look it up in
        # the database.
        if SHA1_RE.search(activation_key):
            try:
                profile = self.get(activation_key=activation_key)
            except self.model.DoesNotExist:
                return False, False
            if not profile.activation_key_expired() \
                                and profile.status == 'authorized':
                user = profile.user
                user.is_active = True
                user.save()
                profile.status = 'activated'
                profile.save()
                user_activated.send(sender=self.model, user=user)
                return user, profile.redirect_to
        return False, False

    def create_inactive_user(self, username, password, email,
                            send_email=True, redirect_to=None, authorize=None):
        """
        Create a new, inactive ``User``, generate a
        ``RegistrationProfile`` and email its activation key to the
        ``User``, returning the new ``User``.

        To disable the email, call with ``send_email=False``.

        The activation email will make use of two templates:

        ``registration/activation_email_subject.txt``
            This template will be used for the subject line of the
            email. It receives one context variable, ``site``, which
            is the currently-active
            ``django.contrib.sites.models.Site`` instance. Because it
            is used as the subject line of an email, this template's
            output **must** be only a single line of text; output
            longer than one line will be forcibly joined into only a
            single line.

        ``registration/activation_email.txt``
            This template will be used for the body of the email. It
            will receive three context variables: ``activation_key``
            will be the user's activation key (for use in constructing
            a URL to activate the account), ``expiration_days`` will
            be the number of days for which the key will be valid and
            ``site`` will be the currently-active
            ``django.contrib.sites.models.Site`` instance.

        To execute customized logic once the new ``User`` has been
        created, connect a function to the signal
        ``registration.signals.user_registered``; this signal will be
        sent (with the new ``User`` as the value of the keyword
        argument ``user``) after the ``User`` and
        ``RegistrationProfile`` have been created, and the email (if
        any) has been sent..

        """
        from registration.signals import user_registered

        new_user = User.objects.create_user(username, email, password)
        new_user.is_active = False
        new_user.save()

        if authorize is None:
            authorize = getattr(settings, 'REGISTRATION_AUTHORIZATION', False)


        registration_profile = self.create_profile(new_user, redirect_to,
                                                                    authorize)
        if send_email is None:
            send_email = getattr(settings, 'REGISTRATION_SEND_EMAIL', True)

        if send_email:
            if authorize:
                self.send_registered_email(new_user)
            else:
                self.send_activation_email(new_user)

        user_registered.send(sender=self.model, user=new_user)
        return new_user
    create_inactive_user = transaction.commit_on_success(create_inactive_user)

    def send_activation_email(self, user):
        """
        Send email with activation code to an authorized user.
        """
        registration_profile = self.get(user=user)
        make_message(
            'registration/activation_email_subject.txt',
            'registration/activation_email.txt',
            [user.email],
            extra_context={
                'activation_key': registration_profile.activation_key,
                'expiration_days': settings.ACCOUNT_ACTIVATION_DAYS,
                'user': user,
            },
            html=getattr(settings, 'REGISTRATION_EMAIL_HTML', False),
            send=True)

    def send_registered_email(self, user):
        """
        Send email to registered but not yet authorized user.
        """
        make_message(
            'registration/registration_email_subject.txt',
            'registration/registration_email.txt',
            [user.email],
            extra_context={
                'user': user,
            },
            html=getattr(settings, 'REGISTRATION_EMAIL_HTML', False),
            send=True)

    def create_profile(self, user, redirect_to, authorize=None):
        """
        Create a ``RegistrationProfile`` for a given
        ``User``, and return the ``RegistrationProfile``.

        The activation key for the ``RegistrationProfile`` will be a
        SHA1 hash, generated from a combination of the ``User``'s
        username and a random salt.

        """
        if authorize is None:
            authorize = getattr(settings, 'REGISTRATION_AUTHORIZATION', False)

        if authorize:
            activation_key = ''
            status = 'not-authorized'
        else:
            salt = sha_constructor(str(random.random())).hexdigest()[:5]
            activation_key = sha_constructor(salt+user.username).hexdigest()
            status = 'authorized'

        return self.create(user=user,
                           activation_key=activation_key,
                           redirect_to=redirect_to,
                           status=status)

    def authorize(self, user, send_email=None):
        from registration.signals import user_authorized

        salt = sha_constructor(str(random.random())).hexdigest()[:5]
        activation_key = sha_constructor(salt+user.username).hexdigest()

        user.registration_profile.status = 'authorized'
        user.registration_profile.activation_key = activation_key
        user.registration_profile.save()

        if send_email is None:
            send_email = getattr(settings, 'REGISTRATION_SEND_EMAIL', True)

        if send_email:
            self.send_activation_email(user)

        user_authorized.send(sender=self.model, user=user)


    def delete_expired_users(self):
        """
        Remove expired instances of ``RegistrationProfile`` and their
        associated ``User``s.

        Accounts to be deleted are identified by searching for
        instances of ``RegistrationProfile`` with expired activation
        keys, and then checking to see if their associated ``User``
        instances have the field ``is_active`` set to ``False``; any
        ``User`` who is both inactive and has an expired activation
        key will be deleted.

        It is recommended that this method be executed regularly as
        part of your routine site maintenance; this application
        provides a custom management command which will call this
        method, accessible as ``manage.py cleanupregistration``.

        Regularly clearing out accounts which have never been
        activated serves two useful purposes:

        1. It alleviates the ocasional need to reset a
           ``RegistrationProfile`` and/or re-send an activation email
           when a user does not receive or does not act upon the
           initial activation email; since the account will be
           deleted, the user will be able to simply re-register and
           receive a new activation key.

        2. It prevents the possibility of a malicious user registering
           one or more accounts and never activating them (thus
           denying the use of those usernames to anyone else); since
           those accounts will be deleted, the usernames will become
           available for use again.

        If you have a troublesome ``User`` and wish to disable their
        account while keeping it in the database, simply delete the
        associated ``RegistrationProfile``; an inactive ``User`` which
        does not have an associated ``RegistrationProfile`` will not
        be deleted.

        """
        for profile in self.all():
            if profile.activation_key_expired():
                user = profile.user
                if not user.is_active:
                    user.delete()

    def authorized(self):
        return self.filter(status='authorized')

    def unauthorized(self):
        return self.filter(status='not-authorized')


class RegistrationProfile(models.Model):
    """
    A simple profile which stores an activation key for use during
    user account registration.

    Generally, you will not want to interact directly with instances
    of this model; the provided manager includes methods
    for creating and activating new accounts, as well as for cleaning
    out accounts which have never been activated.

    While it is possible to use this model as the value of the
    ``AUTH_PROFILE_MODULE`` setting, it's not recommended that you do
    so. This model's sole purpose is to store data temporarily during
    account registration and activation.

    """
    STATUSES = (
        ('not-authorized', _('Not authorized')),
        ('autorized', _('Authorized')),
        ('activated', _('Activated')),
    )

    user = models.OneToOneField(User, verbose_name=_('user'),
                                        related_name='registration_profile')
    activation_key = models.CharField(_('activation key'), max_length=40, blank=True)
    redirect_to = models.CharField(_('redirect to'), max_length=100, blank=True)
    status = models.CharField(_('status'), choices=STATUSES, max_length=25)

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

        Key expiration is determined by a two-step process:

        1. If the user has already activated, the key will have been
           reset to the string constant ``ACTIVATED``. Re-activating
           is not permitted, and so this method returns ``True`` in
           this case.

        2. Otherwise, the date the user signed up is incremented by
           the number of days specified in the setting
           ``ACCOUNT_ACTIVATION_DAYS`` (which should be the number of
           days after signup during which a user is allowed to
           activate their account); if the result is less than or
           equal to the current date, the key has expired and this
           method returns ``True``.

        """
        expiration_date = datetime.timedelta(days=settings.ACCOUNT_ACTIVATION_DAYS)
        return self.status == 'activated' or \
               (self.user.date_joined + expiration_date <= datetime.datetime.now())
    activation_key_expired.boolean = True
