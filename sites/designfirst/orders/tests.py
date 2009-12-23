"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""
from django.conf import settings
from django.db import models
from django.test import TestCase
from django.contrib.auth.models import User
from django.http import HttpRequest

from models import BaseOrderManager, BaseOrder, WorkingOrder 
from forms import SubmitForm


PRO_PRICE = 85
PPACK_PRICE = 125
RUSH_FEE = 20

class ManagerTests(TestCase):
    
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
        
    def test_create_order_as_invalid_user(self):
        user = User.objects.create_user('test', 'test@test.com', 'test')
        user.save()
        
        try:
            order = WorkingOrder.objects.create_order(user, 'test project')
            self.fail('create-fail')
            order.save()
            self.fail('save-fail')
        except:
            pass
        
    def test_create_order_as_dealer(self):        
        user = User.objects.create_user('test', 'test@test.com', 'test')
        user.is_staff = True
        user.save()
        
        order = WorkingOrder.objects.create_order(user, 'test project')
        order.save()
        
class SubmitFormTest(TestCase):
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
        
    def test_submitform_submitted_order(self):
        # submit invalid orders
        # -- already submitted
        data = dict(rush=False, client_notes="this is a test", design_product="1", tracking_code='1', project_name='foo', project_type='K' )
        form = SubmitForm(data, instance=WorkingOrder.objects.get(pk=1))
        self.failIf(form.is_valid())
        
    def test_submitform_incomplete_order(self):
        # submit invalid orders
        # -- incomplete - no attachments        
        data = dict(rush=False, client_notes="this is a test", design_product="1", tracking_code='1', project_name='foo', project_type='K' )
        form = SubmitForm(data, instance=WorkingOrder.objects.get(pk=2))
        self.failIf(form.is_valid())
        
    def test_submitform_broke_user(self):
        self.fail()
        
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
