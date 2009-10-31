from designfirst.home.models import *
from django.contrib import admin

class ApplianceInline(admin.TabularInline):
    model = OrderAppliance

class AttachmentInline(admin.StackedInline):
    model = OrderAttachment
    
class DesignOrderAdmin(admin.ModelAdmin):
    date_hierarchy = 'submitted'
    list_display = ('id','status','client_account', 'project_name', 'client_review_rating' )
#    list_editable = ('status',)
    list_filter = ('status','client_review_rating')
    radio_fields = {"client_review_rating": admin.VERTICAL}
    inlines = [ 
        ApplianceInline, 
        AttachmentInline 
    ]    
    fieldsets = (
        ( None, {
            'fields': ( 'project_name', 'description', 'client_account' )
            }),
        ( 'Design Options', {
            'classes' : [],
            'description' : None,
            'fields' : ( 'color_views', 'elevations', 'quote_cabinet_list' )
            }),
        ( 'Cabinetry Selections', {
            'classes' : [],
            'description' : None,
            'fields' : ( 'manufacturer', 'door_style', 'wood',
                'stain', 'finish_color', 'finish_options', 'cabinetry_notes' )
            }),
        ( 'Door & Drawer Hardware Selections', {
            'classes' : [],
            'description' : None,
            'fields' : ( 'include_hardware', 'door_hardware', 'drawer_hardware' )
            }),
        ( 'Moulding Selections', {
            'classes' : [],
            'description' : None,
            'fields' : ( 'ceiling_height', 'crown_mouldings', 'skirt_mouldings',
                'soffits', 'soffit_height', 'soffit_width', 'soffit_depth' )
            }),
        ( 'Cabinet Box Dimensions', {
            'classes' : [],
            'description' : None,
            'fields' : ( 'stacked_staggered', 'wall_cabinet_height', 'vanity_cabinet_height',
                'vanity_cabinet_depth' )
            }),            
        ( 'Corner Cabinet Selections', {
            'classes' : [],
            'description' : None,
            'fields' : ( 'corner_cabinet_base_bc', 'corner_cabinet_base_bc_direction', 'corner_cabinet_wall_bc',
                'corner_cabinet_wall_bc_direction' )
            }),
        ( 'Island / Peninsula Selections', {
            'classes' : ['collapse'],
            'description' : None,
            'fields' : ( 'island_peninsula_option', )
            }),
        ( 'Other Considerations', {
            'classes' : ['collapse'],
            'description' : None,
            'fields' : ( 'countertop_option', 'backsplash', 'toekick' )
            }),
        ( 'Organization', {
            'classes' : ['collapse'],
            'description' : None,
            'fields' : ( 'lazy_susan', 'slide_out_trays', 'waste_bin', 'wine_rack', 'plate_rack', 'appliance_garage' )
            }),
        ( 'Miscellaneous', {
            'classes' : ['collapse'],
            'description' : None,
            'fields' : ( 'corbels_brackets', 'valance', 'legs_feet', 'glass_doors', 'range_hood', 'posts' )
            }),
        ( 'Notes', {
            'classes' : ['collapse'],
            'description' : None,
            'fields' : ( 'miscellaneous_notes', )
            }),
        ( 'Diagrams', {
            'classes' : [],
            'description' : None,
            'fields' : ( 'client_diagram', 'client_diagram_notes', 'client_diagram_source' )
            }),
        ( 'Rating', {
            'classes' : [],
            'description' : None,
            'fields' : ( 'client_review_rating', 'client_review_notes' )
            }),
        # ( 'Tracking', {
        #     'classes' : [],
        #     'description' : None,
        #     'fields' : ( 'created', 'submitted', 'assigned', 'completed', 'closed', 'modified', 'tracking_notes' )
        #     })
    )                        
        

admin.site.register(DesignOrder, DesignOrderAdmin)
admin.site.register(OrderAppliance)
admin.site.register(OrderAttachment)
admin.site.register(OrderNotes)
admin.site.register(DealerOrganization)

admin.site.register(Transaction)
admin.site.register(UserProfile)


