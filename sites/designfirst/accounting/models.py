from datetime import datetime

from django.db import models
from django.db import transaction
from django.utils.translation import ugettext, ugettext_lazy as _

from customer.models import Dealer

# Create your models here.
DEBIT, CREDIT = ( 'D', 'C')
DC_CHOICES=((DEBIT, _('Debit')), (CREDIT,_('Credit')))

ACCT_CREDIT, CASH = ('A', 'S')
TRANS_TYPE_CHOICES = ((ACCT_CREDIT, _('Account Credit')), (CASH, _('Cash')))
        
class Transaction(models.Model): # TODO --> invoice becomes transaction
    trace_id = models.CharField(max_length=50)
    account = models.ForeignKey(Dealer)
    debit_or_credit = models.CharField(max_length=1, choices=DC_CHOICES)
    trans_type = models.CharField(max_length=1, choices=TRANS_TYPE_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=50)
    timestamp = models.DateTimeField(auto_now_add=True)

@transaction.commit_on_success
def register_purchase(trace, cust_account, price, credit):
    tx1 = Transaction(
        trace_id=trace,
        account=cust_account,
        debit_or_credit=CREDIT, # TODO: verify correct use of CREDIT
        trans_type=CASH,
        amount=price,   # TODO: price schedule lookup,
        description='Web purchase of %s for %s' % ('',price)
    )
    tx2 = Transaction(
        trace_id=trace,
        account=cust_account,
        debit_or_credit=CREDIT, # TODO: verify correct use of CREDIT
        trans_type=ACCT_CREDIT,
        amount=credit,
        description='Account credit of %s for %s' % ('', credit)
    )
    tx1.save()
    tx2.save()

    # add the credit to the customer account
    cust_account.credit_balance += credit
    cust_account.save()

@transaction.commit_on_success
def register_design_order(user, account, order, cost):
    now = datetime.utcnow()
    # update account
    account.credit_balance = account.credit_balance - cost
    account.save()   
    # log transaction
    tx = Transaction(
        account = account,
        amount = cost,
        debit_or_credit = 'C',
        trans_type = 'C',
        description = 'design credit purchase for design order #%s' % order.id,
        timestamp = now
    )
    tx.save()                        

