from django.conf.urls.defaults import *

from product.models import Product

products_dict = { 'queryset': Product.objects.filter(product_type=Product.Const.BASE) }

urlpatterns = patterns('product.views', 

                        url(r'^product/(?P<prodid>\d+)/$', 
                            'product_detail', 
                            name='product-detail'),

                        url(r'^select_products/', 
                            'select_products', 
                            kwargs= { 'template': "product/product_selection.html" ,
                                     'extra_context': dict(selection=True), 
                                     },
                            name='select_products' ),
                            
                        url(r'^confirm_selections/', 
                            'select_products', 
                            kwargs= { 'template': "product/product_selection.html" ,
                                     'extra_context': dict(selection=False), 
                                     },
                            name='confirm_purchase_selections'),
                            
                        url(r'^checkout/', 'checkout', name='checkout'), 
                        url(r'^pp_checkout/', 'paypal_checkout', name='paypal-checkout'), 
                        url(r'^pp_checkout/', 'paypal_checkout', {'phase': 'confirm'}, name='paypal-checkout-confirm'), 
                        
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
