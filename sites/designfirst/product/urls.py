from django.conf.urls.defaults import *

from product.models import Product

products_dict = { 'queryset': Product.objects.filter(purchaseable=True) }

urlpatterns = patterns('product.views', 
                       url(r'^list/', 'product_list', name='product-list'),
                       url(r'^product/(?P<prodid>\d+)/$', 'product_detail', name='product-detail'),
                       url(r'^product/(?P<prodid>\d+)/purchase$', 
                            'product_purchase', name='product-purchase'),
                    )                                              
