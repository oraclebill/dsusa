from django.contrib import admin
from models import *

class ItemTypeInline(admin.TabularInline):
    model = ItemType

class AttributeTypeInline(admin.StackedInline):
    model = AttributeType
    
class ItemInline(admin.TabularInline):
    model = Item

class AttributeInline(admin.StackedInline):
    model = Attribute

class CatalogAdmin(admin.ModelAdmin):
    model = Catalog
    inlines = [ItemTypeInline, AttributeTypeInline, ItemInline]
    
class ItemAdmin(admin.ModelAdmin):
    model = Item
    inlines = [ AttributeInline ]
    
    
admin.site.register(Catalog, CatalogAdmin)
admin.site.register(Item, ItemAdmin)
