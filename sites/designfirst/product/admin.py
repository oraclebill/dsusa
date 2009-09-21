from designfirst.product.models import *
from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    pass
    
class PriceScheduleEntryInline(admin.TabularInline):
    model = PriceScheduleEntry

class PriceScheduleAdmin(admin.ModelAdmin):
    inlines = ( PriceScheduleEntryInline, )
    

admin.site.register(Product,ProductAdmin)
admin.site.register(PriceSchedule,PriceScheduleAdmin)
