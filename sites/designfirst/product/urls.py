from django.conf.urls.defaults import *

from product.models import Product

products_dict = { 'queryset': Product.objects.filter(purchaseable=True) }

urlpatterns = patterns('product.views', 

                        url(r'^product/(?P<prodid>\d+)/$', 
                            'product_detail', 
                            name='product-detail'),

                        url(r'^select_products/', 
                            'select_products', 
                            kwargs= { 'template': "product/product_selection.html" },
                            name='select_products'),
                            
                        url(r'^confirm_selections/', 
                            'select_products', 
                            kwargs= { 'template': "product/product_selection_review.html" },
                            name='confirm_purchase_selections'),
                            
                        url(r'^review_payment_info/', 
                            'review_and_process_payment_info', 
                            name='review_and_process_payment_info'),
                        
                        # url(r'^confirm_payment_info/', 
                        #     'confirm_payment_info', 
                        #     name='confirm_payment_info'),
                        # 
                        # url(r'^process_payment/', 
                        #     'process_payment', 
                        #     name='process_payment'),
                        # 
                        #     
                    )                                              
