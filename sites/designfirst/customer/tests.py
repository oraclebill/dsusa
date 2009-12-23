"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.conf.urls.defaults import *

from models import Dealer, UserProfile
import views as cust_views

def create_dealer_and_user(name, status):
    user = User.objects.create_user(name, '%s@test.com' % name, name)
    company = Dealer.objects.create(
                legal_name=' %s - test dealer' % name,
                status=status,
                email='%s_dealer@test.com' % name,
                credit_balance=500
    )
    profile = UserProfile.objects.create(
                user = user,
                account = company,
                primary = True
    )
                         
class TestUserClasses(TestCase):
            
    def setUp(self):
        create_dealer_and_user('active', Dealer.Const.ACTIVE)
        # 
        name = 'plain-user'
        user = User.objects.create_user(name, '%s@test.com' % name, name)
        #                
        name = 'staff-user'
        user = User.objects.create_user(name, '%s@test.com' % name, name)
        user.is_staff = True
        user.save()        
                        
    def test_view_with_login(self):
        "Request a page that is protected with @login_required"
        
        # Get the page without logging in. Should result in 302.
        response = self.client.get('/dealer/')
        self.assertRedirects(response, 'http://testserver/accounts/login/?next=/dealer/')

    def test_login_form_invalid_user(self):
        post_data = {
            'username': 'Hello World',
            'password': 'foo@example.com',
            'next': '/dealer/',
        }
        response = self.client.post('/accounts/login/', post_data)
        self.assertContains(response, 'errorlist')        
        
    def test_invalid_login(self):
        self.failIf(self.client.login(username='invalid', password='not actually a valid user'))        
        
    def validate_userstatus_redirect(self, username, status, redirect):
        create_dealer_and_user(username, status)
        self.client.login(username=username, password=username)
        response = self.client.get('/dealer/')
        self.assertRedirects(response, redirect)
    
    def test_cancelled_user(self):
        self.validate_userstatus_redirect( 'cancelled', Dealer.Const.CANCELLED, '/inactive/' )
        
    def test_suspended_user(self):
        self.validate_userstatus_redirect( 'suspended', Dealer.Const.SUSPENDED, '/suspended/' )
        
    def test_pending_user(self):
        self.validate_userstatus_redirect( 'pending', Dealer.Const.PENDING, '/pending/' )
            
    def test_archived_user(self):
        self.validate_userstatus_redirect( 'archived', Dealer.Const.ARCHIVED, '/inactive/' )
            
    def test_active_user(self):
        self.failUnless(self.client.login(username='active', password='active'))
        # access /dealer/ w/o redirect 
        response = self.client.get('/dealer/')
        self.assertEquals(response.status_code, 200) 
        # validate some page content
        self.assertContains(response, 'Working Orders')
        self.assertContains(response, reverse('dealer-dashboard'))
        self.assertContains(response, reverse('profile-edit'))
        self.assertContains(response, reverse('create-order'))
        self.assertContains(response, response.context['request'].user.get_profile().account.legal_name)
        # 
            
    
class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.failUnlessEqual(1 + 1, 2)

__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

