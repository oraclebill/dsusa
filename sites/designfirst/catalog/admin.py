from django.contrib import admin
from models import *

class ItemTypeInline(admin.TabularInline):
    model = ItemType

class AttributeTypeInline(admin.TabularInline):
    model = AttributeType
    
class ItemInline(admin.TabularInline):
    model = Item
    exclude = ['description']

class AttributeInline(admin.TabularInline):
    model = Attribute
    exclude = ['description']

class CatalogAdmin(admin.ModelAdmin):
    model = Catalog
    inlines = [ItemInline]

class AttributeTypeAdmin(admin.ModelAdmin):
    model = AttributeType
    inlines = [ AttributeInline ]

class ItemTypeAdmin(admin.ModelAdmin):
    model = ItemType
    inlines = [ ItemInline ]

class ItemAdmin(admin.ModelAdmin):
    model = Item
    list_display = ['catalog', 'type', 'name',]
    list_display_links = ['name',]
    inlines = [ AttributeInline ]

class AttributeAdmin(admin.ModelAdmin):
    model = Attribute
    list_display = ['catalog', 'type', 'name',]
    list_display_links = ['name',]


admin.site.register(Catalog, CatalogAdmin)
admin.site.register(AttributeType, AttributeTypeAdmin)
admin.site.register(ItemType, ItemTypeAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Attribute, AttributeAdmin)
admin.site.register(RelationshipType)
