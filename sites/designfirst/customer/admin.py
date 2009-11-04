from models import *
from django.contrib import admin

class InvoiceLineInline(admin.TabularInline):
    model = InvoiceLine
    
class InvoiceAdmin(admin.ModelAdmin):
    sort = [
        'created'
        ]
    list_display = [
        'id', 
        'created', 
        'status', 
        'customer'
        ]
    inlines = [
        InvoiceLineInline,
        ]

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Dealer)
admin.site.register(UserProfile)


