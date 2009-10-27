from models import WorkingOrder
from django.contrib import admin


class WorkingOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'owner', 'status', 'project_name']
    
admin.site.register(WorkingOrder, WorkingOrderAdmin)