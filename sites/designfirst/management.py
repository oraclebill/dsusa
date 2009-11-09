from customer import models as customer
from django.core.mail import mail_managers, send_mail
from django.core.urlresolvers import reverse
from django.db.models import signals as dbsignals
from django.template.loader import render_to_string
from django.utils.translation import ugettext_noop as _
from notification import models as notification
from orders import models as orders, signals as order_signals
import logging

EMAIL_FROM='no-reply@designserviceusa.com'
EMAIL_SUPPORT='support@designserviceusa.com'

logger = logging.getLogger('management')

class IllegalStateException(Exception):
    pass

def create_notice_types(app, created_models, verbosity, **kwargs):
    notification.create_notice_type(
        "registration_ack", 
        _("Thanks for registering!"), 
        _("Your registration has been recieved.")
    )
    notification.create_notice_type(
        "new_dealer_welcome", 
        _("Welcome to Design Service USA"), 
        _("Your regisration has been processed.")
    )
    notification.create_notice_type(
        "fax_document_ack", 
        _("FAX Document Recieved"), 
        _("A fax document has been recieved.")
    )
    notification.create_notice_type(
        "order_submission_ack", 
        _("Order Submitted"), 
        _("Thanks for your order.")
    )
    notification.create_notice_type(
        "order_clarification_needed", 
        _("Clarification Required"), 
        _("We require additional information to process your order.")
    )
    notification.create_notice_type(
        "completed_order_waiting", 
        _("Design Order Completed"), 
        _("Your completed design is waiting.")
    )
    notification.create_notice_type(
        "payment_reciept", 
        _("Payment Receipt"), 
        _("A reciept for your recent purchase.")
    )
    notification.create_notice_type(
        "subscription_renewal_reminder", 
        _("Time to renew!"), 
        _("Your subscription will end soon. Time to renew!")
    )
dbsignals.post_syncdb.connect(create_notice_types, sender=notification)
 
def new_dealer_notification(sender, **kwargs):
    "When a new dealer appears, send a 'thanks for registering' email"
    if not kwargs.get('created'):
        return        
    dealer = kwargs.get('instance')  
    if not dealer.email:
        mail_managers(
            'New dealer %s requires manual validation - email blank' % dealer.legal_name,
            'Dealer email blank' 
        )
        return            
    mail_managers('New dealer registration - %s' % dealer.legal_name, '/service/registrations/%s' % dealer.id  )
    #    # the notification infrastructure needs a 'User'...
    #    notification.send([dealer], 'registration_ack', locals())
    context = {'name': dealer.legal_name }
    subject = render_to_string( 'notification/registration_ack/short.txt', context)
    message = render_to_string( 'notification/registration_ack/full.txt', context)
    recipients = [dealer.email, EMAIL_SUPPORT]
    rep = dealer.account_rep
    if rep:
        recipients.append(rep.email)        
    send_mail(subject, message, EMAIL_FROM, recipients)
          
dbsignals.post_save.connect(new_dealer_notification, sender=customer.Dealer)        
        
def new_fax_notification(sender, **kwargs):
    "When a new fax appears, send a 'got it!' email"
    created = kwargs.get('created')
    if not created:
        return     
    attachment = kwargs.get('instance')  
    if attachment and not attachment.order:
        mail_managers(
            'New attachment %s requires manual validation - blank order' % attachment,
            'No associated order for attachment %s' % attachment.id
        )
        return        
    if attachment.source == attachment.FAXED:        
        context = {'document': attachment, 'order': attachment.order }
        notification.send([attachment.order.owner], 'fax_document_ack', context)    
dbsignals.post_save.connect(new_fax_notification, sender=orders.Attachment)        


def new_order_notification(sender, **kwargs):
    "When a new order appears, send a 'got it!' email"
    order = sender
    if not order:
        raise IllegalStateException()
    status = kwargs.get('new')
    if not status:
        raise IllegalStateException()
    if status != orders.WorkingOrder.SUBMITTED:
        return
    # TODO: Don't send notices for events that have already been signaled
    #       I think we can extend the Notice framework to have a generic FK 
    #       - notice_subject. If we find a notice for 'this' thing, don't repeat notification.
    if not order.owner:
        mail_managers(
            'New order %s requires manual validation - blank owner' % order,
            'No associated owner for order %s' % order.id
        )
        return        
    notification.send([order.owner], 'order_submission_ack', locals())
    mail_managers('Order Submission Notice - order #%s for %s' % (order, order.owner.get_profile().account.legal_name), '')
order_signals.status_changed.connect(new_order_notification)        
    
def completed_order_notification(sender, **kwargs):
    "When a new order appears, send a 'got it!' email"
    order = sender
    if not order:
        raise IllegalStateException() 
    if order.status != orders.WorkingOrder.COMPLETED:
        return
    # TODO: Don't send notices for events that have already been signaled
    #       I think we can extend the Notice framework to have a generic FK 
    #       - notice_subject. If we find a notice for 'this' thing, don't repeat notification.    
    if not order.owner:
        mail_managers(
            'New order %s requires manual validation - blank owner' % order,
            'No associated owner for order %s' % order.id
        )
        return        
    notification.send([order.owner], 'completed_order_waiting', locals())
    mail_managers('Order Completion Notice - order #%s for %s' % (order, order.owner.get_profile().account.legal_name), '')
order_signals.status_changed.connect(completed_order_notification)        
    
    
    