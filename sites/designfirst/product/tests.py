"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.http import HttpRequest

from models import Product
from product.models import ProductRelationship
from product.cart import new_cart
import views

class FixtureTest(TestCase):
    "Verify initial data includes core products"
    def test_has_base_products(self):
        products = Product.objects.filter(product_type__contains=Product.Const.BASE)
        self.failUnless(products)
        
    def test_has_optional_products(self):
        products = Product.objects.filter(product_type__contains=Product.Const.OPTION)
        self.failUnless(products)
        
    def test_has_subscription_products(self):
        products = Product.objects.filter(product_type__contains=Product.Const.SUBSCRIPTION)
        self.failUnless(products)
        
    def test_has_package_products(self):
        products = Product.objects.filter(product_type__contains=Product.Const.PACKAGE)
        self.failUnless(products)
        
    def test_has_base_bundles(self):
        # prodcuts with
        products = Product.objects.filter(product_type__contains=Product.Const.BASE, source_set__deptype=ProductRelationship.Const.COMPOSED_OF)
        self.failUnless(products)

    def test_has_option_bundles(self):
        products = Product.objects.filter(product_type__contains=Product.Const.OPTION, source_set__deptype=ProductRelationship.Const.COMPOSED_OF)
        self.failUnless(products)
        
    def test_has_no_subscription_bundles(self):
        products = Product.objects.filter(product_type__contains=Product.Const.SUBSCRIPTION, source_set__deptype=ProductRelationship.Const.COMPOSED_OF)
        self.failIf(products)
        

class ModelTest(TestCase):
    "Test basic model functionality"
    pass
        
        
class CartTest(TestCase):
    "Test shopping cart functionality"
    pass
        

class ViewTest(TestCase):
    "Test view methods"
    
    def setUp(self):
        pass

    def testProductDetail(self):
        response = self.client.get('/')
        product = Product.objects.all()[0]   
        self.client.login()       
        response = self.client.get('/product/%d' % product.id)  
        print response
        self.assertContains(response, product.name)

    def testSelectProducts(self):
        pass
    
    def testReviewAndProcessPaymentInfo(self):
        pass
    
    def test_product_purchase(self):
        """
        product purchase screen is available to dealers in 'active' status and 
        displays a product list form
        """
        
class TestCaseTemplate(TestCase):
    urls = 'test.urls'  # root urlconf for testing
    fixtures = ['test-data.json', 'more-test-data', ]
     
    def xsetUp(self):
        pass
    
    def xtestTemplate(self):
        # ajax request
        response = self.client.get('/profiles/1', follow=False, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        if response.is_ajax():
            pass
        
        response = self.client.get('/profiles/1', follow=True, data={'foo': 'bar'})
        if response.redirect_chain:
            pass
        
        response = self.client.get('/profiles/1', content_type='text/xml')
        
#        self.client.post('/orders/1/new', data={}, content_type, follow)
#        self.client.login()
#        self.client.logout()
#        
#        self.assertContains(response, text, count, status_code)
#        self.assertNotContains(response, text, status_code)
#        self.assertFormError(response, form, field, errors)
#        self.assertTemplateUsed(response, template_name)
#        self.assertTemplateNotUsed(response, template_name)
#        self.assertRedirects(response, expected_url, status_code, target_status_code, host)
        
        
        
            
