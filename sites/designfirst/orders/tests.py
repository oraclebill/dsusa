"""
Tests basic functionality of the orders module.
"""
from django.conf import settings
from django.core.urlresolvers import *
from django.db import models, transaction
from django.test import TestCase, TransactionTestCase as BaseTransactionTestCase
from django.contrib.auth.models import User
from django.http import HttpRequest
from django.core.exceptions import ValidationError

from customer.models import Dealer, create_basic_dealer_account 


from models import BaseOrderManager, BaseOrder, WorkingOrder 
from forms import SubmitForm
from signals import status_changed

PRO_PRICE = 85
PPACK_PRICE = 125
RUSH_FEE = 20


class TransactionTestCase(BaseTransactionTestCase):
    def _fixture_teardown(self):
        transaction.rollback()
    
class OrderTests(TestCase):
    def setUp(self):
        self.testuser = User.objects.create_user('test-user', 'test@test.com', 'test-user')

    def test_save_hits_database(self):
        order = WorkingOrder()
        order.owner = self.testuser
        order.account_code = 'test-account-code'
        order.project_name = 'test-project-name'
        order.save()
        orderid = order.id
        
        self.failUnless(WorkingOrder.objects.get(pk=orderid))
        
    def test_ownerless_order(self):
        
        # fail if owner not set
        order = WorkingOrder()
        order.account_code = 'test-account-code'
        order.project_name = 'test-project-name'
        #order.owner = self.testuser
        self.failUnlessRaises(Exception, order.save)

        order = WorkingOrder(account_code='test-account-code', project_name = 'test-project-name')
        self.failUnlessRaises(Exception, order.save)
    
    def test_projectless_order(self):
        
        # fail if no project
        order = WorkingOrder()
        order.account_code = 'test-account-code'
        order.owner = self.testuser
        self.failUnlessRaises(ValidationError, order.save)

        order = WorkingOrder(owner=self.testuser, account_code='test-account-code')
        self.failUnlessRaises(ValidationError, order.save)
    
    def test_accountless_order(self):
        # fail if owner not set
        order = WorkingOrder()
        #order.account_code = 'test-account-code'
        order.project_name = 'test-project-name'
        self.failUnlessRaises(ValidationError, order.save)
    
        order = WorkingOrder(owner=self.testuser, project_name = 'test-project-name')
        self.failUnlessRaises(ValidationError, order.save)

    def test_minimal_order(self):
        order = WorkingOrder()
        order.owner = self.testuser
        order.account_code = 'test-account-code'
        order.project_name = 'test-project-name'
        order.save()
        
        order = WorkingOrder(owner=self.testuser, account_code='test-account-code', project_name = 'test-project-name')
        order.save()
        

    def test_status_change(self):
        # create a listener for the 'status_changed' event
        update = [0, None]        
        def handle_event(sender, **kwargs):
            print 'fired...'
            update[0] += 1
            update[1] = kwargs

        def validate_order_status(inst, count, old, new):
            self.failUnlessEqual(inst.status, new)
            self.failUnlessEqual(update[1]['old'], old)
            self.failUnlessEqual(update[1]['new'], new)
            self.failUnlessEqual(update[0], count)
            
        # register as a listener
        status_changed.connect(handle_event)
        self.failUnlessEqual(update[0], 0, 'initially counter is zero')
        
        # create a new order, verify counter incremented
        save_counter = 0
        order = WorkingOrder(owner=self.testuser, account_code='test-account-code', project_name = 'test-project-name')
        order.save(); save_counter += 1    # 1   
        validate_order_status(order, save_counter, None, BaseOrder.Const.DEALER_EDIT)
        
        # retrieve a copy of the order, verify counter incremented only after save
        order_copy = WorkingOrder.objects.get(pk=order.id)
        order_copy.status = BaseOrder.Const.SUBMITTED
        self.failUnlessEqual(update[0], save_counter)
        order_copy.save(); save_counter += 1   # 2    
        validate_order_status(order_copy, save_counter, BaseOrder.Const.DEALER_EDIT, BaseOrder.Const.SUBMITTED)

        # retrieve a copy of the order, verify counter not incremented  when update doesn't modify value
        copy2 = WorkingOrder.objects.get(pk=order.id)
        copy2.status = BaseOrder.Const.SUBMITTED
        copy2.save(); save_counter += 1   # 3  
        self.failUnlessEqual(update[0], save_counter - 1)  # this save shouldn't have counted  
        
        # update original order.. again..
        order.status = BaseOrder.Const.ASSIGNED
        order.save()
        validate_order_status(order, save_counter, BaseOrder.Const.SUBMITTED, BaseOrder.Const.ASSIGNED)
        
#class ManagerTests(TestCase):
class ManagerTests():
    
    def test_create_order_as_admin(self):
        user = User.objects.create_user('test', 'test@test.com', 'test')
        user.is_staff = True
        user.save()
        
        # using defaults
        order = WorkingOrder.objects.create_order(user, 'test project')
        order.save()
        self.failUnless(order.tracking_code)
        self.failUnlessEqual(order.account_code, user.username)
        self.failUnlessEqual(order.project_name, 'test project')
        self.failUnlessEqual(order.project_type, BaseOrder.Const.KITCHEN_DESIGN)
        
        # using explicit type, tracking code and account code
        order = WorkingOrder.objects.create_order(user, 'test project #2', account_code='TEST-ACCT-1', tracking_code='TEST-TRACK-001')
        order.save()
        self.failUnlessEqual(order.tracking_code,'TEST-TRACK-001')
        self.failUnlessEqual(order.account_code, 'TEST-ACCT-1')
        self.failUnlessEqual(order.project_name, 'test project #2')
        self.failUnlessEqual(order.project_type, BaseOrder.Const.KITCHEN_DESIGN)        
        
#    def test_create_order_as_invalid_user(self):
#        user = User.objects.create_user('test', 'test@test.com', 'test')
#        user.save()
#        
#        def create_order_with_invalid_user():
#            order = WorkingOrder.objects.create_order(user, 'test project')
#            order.save()
#        self.failUnlessRaises(Exception, create_order_with_invalid_user)
        
    def test_create_order_as_dealer(self):        
        dealer = create_basic_dealer_account("test-dealer", "dealer", "dealer@dealer.com")        
        order = WorkingOrder.objects.create_order(dealer, 'test project')
        order.save()

        self.failUnless(order.tracking_code, 'empty tracking code')
        self.failUnless(order.account_code, 'empty account code')
        self.failUnlessEqual(order.project_name, 'test project')
        self.failUnlessEqual(order.project_type, BaseOrder.Const.KITCHEN_DESIGN)        
                
                
class LifeCycleTest():
    "Tests the order lifecycle"
    
    def setUp(self):
        self.testuser = User.objects.create_user('test-user', 'test@test.com', 'test-user')
        
    def test_standard_flow(self):
        # create a valid dealer and login
        username, password = 'dealer', 'dealer'
        dealer = create_basic_dealer_account(dealer_name='dealer-%s' % username, 
                                             username=username, 
                                             email='%s@%s.com' % (username, username), 
                                             password=password, 
                                             account_status=Dealer.Const.ACTIVE)
        credentials = (username, password)
        self.failUnless(self.client.login())      
        # create an unsubmittable order (no attachments) and validate I can't submit it        
        order = WorkingOrder.objects.create_order(dealer, 'test project')
        submiturl = reverse('submit-order', args=[order.id])
        data = dict(rush=False, client_notes="this is a test", design_product="1")
        response = self.client.post(submiturl, data)
        self.failUnlessEqual(response.status_code, 200)
        # make the order submittable, validate we can submit it
        # make sure status attributes change appropriately on submisssion
        # validate we cannot submit an already submitted order                
        data = dict(rush=False, client_notes="this is a test", design_product="1", tracking_code='1', project_name='foo', project_type='K' )
        response = self.client.post(submiturl, data)
        self.assertRedirects(response, reverse('submit-order-completed', args=[13]))
        # validate we cannot edit an already submitted order
        # validate we can view/print submitted order without updating timestamps              

                
class SubmitFormTest():
    "Verify Order Submission Form"
    fixtures = ['test_userdata', 'test_orderdata']
    
    def setUp(self):
        pass
        
    def test_test_fixtures(self):
        self.failUnlessEqual(User.objects.get(pk=1).username,'admin' )       
        self.failUnlessEqual(User.objects.get(pk=2).username,'dealer' )       
#        self.failUnlessEqual(Dealer.objects.get(pk=1).legal_name,'Test Dealer' )       
        self.failUnlessEqual(WorkingOrder.objects.get(pk=1).project_name, 'invalid submitted', 'invalid submitted' )   # ..    
        self.failUnlessEqual(WorkingOrder.objects.get(pk=2).project_name, 'incomplete editing', 'incomplete editing' )   # ..    
        self.failUnlessEqual(WorkingOrder.objects.get(pk=13).project_name, 'test submittable', 'test submittable'    )   # ..    
                
#    def test_submitform_incomplete_order(self):
#        # submit invalid orders
#        # -- incomplete - no attachments        
#        data = dict(rush=False, client_notes="this is a test", design_product="1", tracking_code='1', project_name='foo', project_type='K' )
#        form = SubmitForm(data, instance=WorkingOrder.objects.get(pk=2))
#        self.failIf(form.is_valid())
#        
#    def test_submitform_broke_user(self):
#        self.fail()
#        
#    def test_submitform_pro(self):
#        request = HttpRequest()
#        data = dict(rush=False, client_notes="this is a test", design_product="1" , tracking_code='1', project_name='foo', project_type='K' )
#        form = SubmitForm(data, instance=WorkingOrder.objects.get(pk=13))
#        self.failUnless(form.is_valid(), form.errors)
#        
#        order=form.save()
#        self.failUnlessEqual(order.cost, PRO_PRICE)
#        self.failUnlessEqual(order.rush, False)
#        self.failUnlessEqual(order.color_views, False)
#        self.failUnlessEqual(order.elevations, False)
#        self.failUnlessEqual(order.quoted_cabinet_list, False)
#        
#    def test_submitform_presentation_options(self):
#        request = HttpRequest()
#        data = dict(rush=False, client_notes="this is a test", design_product="2" , tracking_code='1', project_name='foo', project_type='K' )
#        form = SubmitForm(data, instance=WorkingOrder.objects.get(pk=13))
#        self.failUnless(form.is_valid(), form.errors)
#        
#        order=form.save()
#        self.failUnlessEqual(order.cost, PPACK_PRICE)
#        self.failUnlessEqual(order.rush, False)
#        self.failUnlessEqual(order.color_views, True)
#        self.failUnlessEqual(order.elevations, True)
#        self.failUnlessEqual(order.quoted_cabinet_list, True)
#        
#    def test_submitform_rush(self):
#        request = HttpRequest()
#        data = dict(rush=True, client_notes="this is a test", design_product="2" , tracking_code='1', project_name='foo', project_type='K' )
#        form = SubmitForm(data, instance=WorkingOrder.objects.get(pk=13))
#        self.failUnless(form.is_valid(), form.errors)
#        
#        order=form.save()
#        self.failUnlessEqual(order.cost, RUSH_FEE+PPACK_PRICE)
#        
#        pass        
