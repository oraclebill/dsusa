from designfirst.product.models import *
from django.contrib import admin

class ProductAdmin(admin.ModelAdmin):
    pass

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['created', 'status', 'customer', 'id']
    
class PriceScheduleEntryInline(admin.TabularInline):
    model = PriceScheduleEntry

class PriceScheduleAdmin(admin.ModelAdmin):
    inlines = ( PriceScheduleEntryInline, )
    

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(PriceSchedule, PriceScheduleAdmin)
