from models import WorkingOrder
from django.contrib import admin


class WorkingOrderAdmin(admin.ModelAdmin):
    list_display = ['updated', 'id', 'owner', 'status', 'project_name']
    
admin.site.register(WorkingOrder, WorkingOrderAdmin)