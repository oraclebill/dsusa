from django.contrib import admin
from models import *

class ProductLineInline(admin.TabularInline):
    model = ProductLine

class DoorStyleInline(admin.StackedInline):
    model = DoorStyle
    
class WoodOptionInline(admin.StackedInline):
    model = WoodOption
    
class FinishOptionInline(admin.StackedInline):
    model = FinishOption
    
class ManufacturerAdmin(admin.ModelAdmin):
    model = Manufacturer
    inlines = [ ProductLineInline ]
    
class ProductLineAdmin(admin.ModelAdmin):
    model = ProductLine
    inlines = [ DoorStyleInline, WoodOptionInline, FinishOptionInline, ]
    
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(ProductLine, ProductLineAdmin)
admin.site.register(DoorStyle)
admin.site.register(WoodOption)
admin.site.register(FinishOption)