import logging

from django.core.mail import mail_managers, send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib.sites.models import Site, RequestSite

logger = logging.getLogger('customer.registration.notification')

def notify_new_dealer_registration(dealer):
    "When a new dealer appears, send a 'thanks for registering' email"
    if not dealer.email:
        logger.info("new_dealer_notification: dealer [%s] has no email, mailing managers", dealer)            
        try:
            mail_managers(
                'New dealer %s requires manual validation - email blank' % dealer.legal_name,
                'Dealer email blank' 
            )
        except Exception as ex:
            logger.error("new_dealer_notification: %s: failed to send new dealer exception email for dealer [%s]", ex, dealer)            
            return            
    

    try:
        
        site = Site.objects.get_current()

        # send dealer acknowledgement
        context = {'name': dealer.legal_name }
        subject = render_to_string( 'notification/registration_ack/short.txt', context)
        message = render_to_string( 'notification/registration_ack/full.txt', context)
        recipients = [dealer.email, settings.SUPPORT_EMAIL]
        rep = dealer.account_rep
        if rep:
            recipients.append(rep.email)    

        send_mail(subject, message, settings.NOREPLY_EMAIL, recipients)
        
        # send admin notification
        context = { 'dealer': dealer, 'site': site }
        subject = render_to_string( 'registration/admin_email_subject.txt', context)
        # Email subject *must not* contain newlines
        subject = ''.join(subject.splitlines())
        message = render_to_string('registration/admin_email.txt', context)

        mail_managers(subject, message)

    except Exception as ex:
        logger.error("new_dealer_notification: %s: failed to send new dealer notification email for dealer [%s]", ex, dealer)            
        
