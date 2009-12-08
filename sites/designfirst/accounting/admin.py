from models import Transaction
from django.contrib import admin

class TransactionAdmin(admin.ModelAdmin):
    list_display = ['timestamp', 'trace_id', 'account', 'debit_or_credit', 'trans_type', 'description'] 
    list_display_links = ['trace_id']
    list_filter = ['debit_or_credit', 'trans_type' ]
    ordering = ['timestamp',]
    search_fields = ['description',]
    radio_fields = {'debit_or_credit': admin.HORIZONTAL, 'trans_type': admin.HORIZONTAL }


admin.site.register(Transaction, TransactionAdmin)
