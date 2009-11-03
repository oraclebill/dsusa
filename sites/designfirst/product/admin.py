from designfirst.product.models import *
from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
