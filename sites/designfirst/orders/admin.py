from models import WorkingOrder, Attachment, AttachPreview
from django.contrib import admin

class AttachmentInline(admin.TabularInline):
    model = Attachment

class AttachPreviewInline(admin.TabularInline):
    model = AttachPreview

class WorkingOrderAdmin(admin.ModelAdmin):
    list_display = ['updated', 'id', 'owner', 'status', 'project_name']
    inlines = [
        AttachmentInline, 
#        AttachPreviewInline  # causes hangs..
    ]

class AttachPreviewAdmin(admin.ModelAdmin):
    list_display = ['page', 'file']
    
admin.site.register(WorkingOrder, WorkingOrderAdmin)
admin.site.register(AttachPreview, AttachPreviewAdmin)