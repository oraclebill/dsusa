
from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from models import Invoice, InvoiceLine, Dealer, UserProfile


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

class DealerAdmin(admin.ModelAdmin):
    model = Dealer
    actions = ['approve_dealers',]
    list_display = ['id', 'status', 'legal_name', 'email']
    
    def approve_dealers(self, request, queryset):
        """
        Approves the selected dealers, providing they are not already approved. 
        Notification emails are sent notififying primary account users of changes.
        """
        for dealer in queryset:
            dealer.approve()
    approve_dealers.short_description = _("Approve dealers")
    
    
class UserProfileAdmin(admin.ModelAdmin):
    model = UserProfile
    list_display = ['user', 'account_legal_name']
    
    def account_legal_name(self, profile_obj):
        return profile_obj.account.legal_name 
    account_legal_name.short_description = 'Company'
    
admin.site.register(Dealer, DealerAdmin)
admin.site.register(Invoice, InvoiceAdmin)
admin.site.register(UserProfile, UserProfileAdmin)


