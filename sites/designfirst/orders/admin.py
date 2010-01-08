from models import WorkingOrder, Attachment, AttachmentPage
from django.contrib import admin

class AttachmentInline(admin.TabularInline):
    model = Attachment

class AttachmentPageInline(admin.TabularInline):
    model = AttachmentPage

class WorkingOrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'account_code', 'project_name', 'status', 'created', 'owner', 'updated', 'submitted' ]
    list_display_links = ['id', 'project_name']
    list_filter = ['owner', 'status' ]
    ordering = ['id',]
    search_fields = ['project_name',]
    #radio_fields = {'status': admin.HORIZONTAL, 'project_type': admin.HORIZONTAL }
    save_as = True
    actions_on_top = True
    
#    fieldsets = (
#        ('Order Information', {
#            'fields': ('account_code', 'tracking_code', 
#                       'project_name', 'owner', 'status',   
#                       'project_type', 
#                       ('rush', 'color_views', 'elevations', 'quoted_cabinet_list'), 'cost', )
#        }),
#    )
    inlines = [
        AttachmentInline, 
#        AttachmentPageInline  # causes hangs..
    ]
    
    def complete_order(self):
        print "Yay!"


class AttachmentAdmin(admin.ModelAdmin):
    list_display = ['order', 'type', 'file', 'source', 'timestamp']
    inlines = [
        AttachmentPageInline, 
#        AttachmentPageInline  # causes hangs..
    ]
    
class AttachmentPageAdmin(admin.ModelAdmin):
    list_display = ['id', 'attachment', 'page', 'file']
    
admin.site.register(WorkingOrder, WorkingOrderAdmin)
admin.site.register(Attachment, AttachmentAdmin)
admin.site.register(AttachmentPage, AttachmentPageAdmin)