from models import WorkingOrder, Attachment, AttachmentPage
from django.contrib import admin

class AttachmentInline(admin.TabularInline):
    model = Attachment

class AttachmentPageInline(admin.TabularInline):
    model = AttachmentPage

class WorkingOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'project_name', 'status', 'updated', 'owner', ]
    inlines = [
        AttachmentInline, 
#        AttachmentPageInline  # causes hangs..
    ]

class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['order', 'type', 'file', 'source', 'timestamp']
    inlines = [
        AttachmentPageInline, 
#        AttachmentPageInline  # causes hangs..
    ]
    
class AttachmentPageAdmin(admin.ModelAdmin):
    list_display = ['page', 'file']
    
admin.site.register(WorkingOrder, WorkingOrderAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(AttachmentPage, AttachmentPageAdmin)