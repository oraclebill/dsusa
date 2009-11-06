from django.conf import settings
from django.utils.translation import ugettext_noop as _

if "notification" in settings.INSTALLED_APPS:
    from notification import models as notification

    def create_notice_types(app, created_models, verbosity, **kwargs):
        notification.create_notice_type("registration_ack", _("Thanks for registering!"), _("Your registration has been recieved."))
        notification.create_notice_type("new_dealer_welcome", _("Welcome to Design Service USA"), _("Your regisration has been processed."))
        notification.create_notice_type("fax_document_ack", _("FAX Document Recieved"), _("A fax document has been recieved."))
        notification.create_notice_type("order_submission_ack", _("Order Submitted"), _("Thanks for your order."))
        notification.create_notice_type("order_clarification_needed", _("Clarification Required"), _("We require additional information to process your order."))
        notification.create_notice_type("completed_order_waiting", _("Design Order Completed"), _("Your completed design is waiting."))
        notification.create_notice_type("payment_reciept", _("Payment Receipt"), _("A reciept for your recent purchase."))
        notification.create_notice_type("subscription_renewal_reminder", _("Time to renew!"), _("Your subscription will end soon. Time to renew!"))

    signals.post_syncdb.connect(create_notice_types, sender=notification)
else:
    print "Skipping creation of NoticeTypes as notification app not found"
 