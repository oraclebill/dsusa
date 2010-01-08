from models import WorkingOrder, Attachment, AttachmentPage
from django.contrib import admin
from django.forms.models import fields_for_model

class AttachmentInline(admin.TabularInline):
    
    model = Attachment
    

class AttachmentPageInline(admin.TabularInline):
    
    model = AttachmentPage
    
    
class OrderNoteInline(admin.ModelAdmin):
    
    model = OrderNote

    list_display = ['author', 'subject', 'date']
    inlines = [
        AttachmentPageInline, 
#        AttachmentPageInline  # causes hangs..
    ]
    

class WorkingOrderAdmin(admin.ModelAdmin):
    
    list_display = ['id', 'project_name', 'account_code', 'status', 'owner', 'created', 'submitted', 'updated', ]
    list_display_links = ['id', 'account_code', 'project_name']
    list_filter = ['owner', 'account_code', 'status' ]
    ordering = ['id',]
    search_fields = ['project_name',]
    #radio_fields = {'status': admin.HORIZONTAL, 'project_type': admin.HORIZONTAL }
    save_as = True
    actions_on_top = True
    
    fieldsets = (
        ('Order Information', {
            'fields': ( 'status', 'account_code', 'tracking_code', 
                       'project_name', 'owner', 'project_type', 
                       ('rush', 'color_views', 'elevations', 'quoted_cabinet_list'), 'cost', )
        }),
#        ('Order Status', {
#            'fields': ('status', 'submitted', 'updated') 
#        }),
    )

    inlines = [
        AttachmentInline, 
#        AttachmentPageInline  # causes hangs..
    ]
    
    def __init__(self, model, admin_site):
        super(WorkingOrderAdmin, self).__init__(model, admin_site)
        fields = fields_for_model(self.model)            
        for fieldname in admin.util.flatten_fieldsets(self.fieldsets):
            fields.pop(fieldname, None) 
        undeclared_fields = (('Design Information', 
                                {'fields': fields.keys() ,
                                 'classes': ('collapse',) } ),)
        self.fieldsets += undeclared_fields

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