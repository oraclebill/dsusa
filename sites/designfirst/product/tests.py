"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from models import Product
from product.models import ProductRelationship

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
        
        
__test__ = {"doctest": """
Another way to test that 1 + 1 is equal to 2.

>>> 1 + 1 == 2
True
"""}

