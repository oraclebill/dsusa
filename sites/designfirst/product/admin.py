from django.contrib import admin
from models import Product, ProductRelationship

class ProductRelationshipInline(admin.TabularInline):
    model = ProductRelationship
    fk_name = 'source'
    exclude = ['description',]
    extra = 1

class ProductAdmin(admin.ModelAdmin):
    ordering = ['sort_order', ]
    list_display = ['name', 'product_type', 'base_price', 'description']
    list_filter = ['product_type', ]
    inlines = [ ProductRelationshipInline, ]

admin.site.register(Product, ProductAdmin)
