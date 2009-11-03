from models import *
from django.contrib import admin

class InvoiceAdmin(admin.ModelAdmin):
    list_display = ['created', 'status', 'customer', 'id']

admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(Dealer)
admin.site.register(UserProfile)


