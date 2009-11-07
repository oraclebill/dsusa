from django.conf import settings
from django.core.mail import send_mail, mail_managers
from django.db.models import signals
from django.template import Template, Context
from django.template.loader import get_template    
from django.utils.translation import ugettext_noop as _

from notification import models as notification

from customer import models as customer
from orders import models as orders

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
signals.post_syncdb.connect(create_notice_types, sender=notification)
 
def new_dealer_notification(model, instance, created, **kwargs):
    "When a new dealer appears, send a 'thanks for registering' email"
    from django.template import Template, Context
    from django.template.loader import get_template    
    if not created:
        return        
    if not instance.email:
        mail_managers(
            'New dealer %s requires manual validation - email blank' % instance.legal_name,
            'Dealer email blank' 
        )
        return        
    # # can't use notification because we don't have a user yet!!
    # template = get_template('notification/registration_ack/full.txt')
    # message = template.render(Context({ 'dealer': instance }))
    # send_mail('Welcome to Design Service USA!', message, 'service@designserviceusa.com',[instance.email])
    # mail_managers('welcome mail sent for %s' % instance.legal_name, message)
    notification.send([instance], 'registration_ack')
signals.post_save.connect(new_dealer_notification, sender=customer.Dealer)        
        
def new_fax_notification(model, attachment, created, **kwargs):
    "When a new fax appears, send a 'got it!' email"
    if not created:
        return        
    if not attachment.order:
        mail_managers(
            'New attachment %s requires manual validation - blank order' % attachment,
            'No associated order for attachment %s' % attachment.id
        )
        return        
    notification.send([attachment.order.owner], 'fax_document_ack')    
signals.post_save.connect(new_fax_notification, sender=orders.Attachment)        


def new_order_notification(model, order, created, **kwargs):
    "When a new order appears, send a 'got it!' email"
    if not order.status == WorkingOrder.SUBMITTED:
        return
    # TODO: Don't send notices for events that have already been signalled
    #       I think we can extend the Notice framework to have a generic FK 
    #       - notice_subject. If we find a notice for 'this' thing, don't repeat notification.
    if not order.owner:
        mail_managers(
            'New order %s requires manual validation - blank owner' % order,
            'No associated owner for order %s' % order.id
        )
        return        
    notification.send([order.owner], 'order_submission_ack')
    mail_managers('Order Submission Notice - order #%s for %s' % (order, order.owner.get_profile().account.legal_name), '')
signals.post_save.connect(new_order_notification, sender=orders.WorkingOrder)        
    
def completed_order_notification(model, order, created, **kwargs):
    "When a new order appears, send a 'got it!' email"
    if not order.status == WorkingOrder.COMPLETED:
        return
    # TODO: Don't send notices for events that have already been signalled
    #       I think we can extend the Notice framework to have a generic FK 
    #       - notice_subject. If we find a notice for 'this' thing, don't repeat notification.    
    if not order.owner:
        mail_managers(
            'New order %s requires manual validation - blank owner' % order,
            'No associated owner for order %s' % order.id
        )
        return        
    notification.send([order.owner], 'completed_order_waiting')
    mail_managers('Order Completion Notice - order #%s for %s' % (order, order.owner.get_profile().account.legal_name), '')
signals.post_save.connect(completed_order_notification, sender=orders.WorkingOrder)        
    
    
    