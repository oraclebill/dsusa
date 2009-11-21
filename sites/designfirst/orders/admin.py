from models import WorkingOrder, Attachment, AttachmentPage
from django.contrib import admin

class AttachmentInline(admin.TabularInline):
    model = Attachment

class AttachmentPageInline(admin.TabularInline):
    model = AttachmentPage

class WorkingOrderAdmin(admin.ModelAdmin):
    list_display = ['updated', 'id', 'owner', 'status', 'project_name']
    inlines = [
        AttachmentInline, 
#        AttachmentPageInline  # causes hangs..
    ]

class AttachmentPageAdmin(admin.ModelAdmin):
    list_display = ['page', 'file']
    
admin.site.register(WorkingOrder, WorkingOrderAdmin)
admin.site.register(AttachmentPage, AttachmentPageAdmin)