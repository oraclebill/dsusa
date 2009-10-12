from django import template
from django.contrib import admin
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.utils.translation import ugettext_lazy as _


from models import *
from forms import CreateOrderForm, EditOrderForm

class ApplianceInline(admin.TabularInline):
    model = OrderAppliance
    extra = 5

class AttachmentInline(admin.StackedInline):
    model = OrderAttachment
    extra = 1
    
class DesignOrderAdmin(admin.ModelAdmin):
    
    date_hierarchy = 'submitted'
    
    list_display = ('id', 'customer', 'project_name', 'status', )
#    list_editable = ('status',)
    list_filter = ('status',)
    inlines = [ 
        ApplianceInline, 
        AttachmentInline 
    ]    
        
    add_fieldsets = (
        ( 'Order Information', {
            'description' : 'Design Order tracking information',
            'fields': ( 'customer', 'received', 'project_name', 'design_type', 
                'color_views', 'elevations', 'price_report', 'addl_notification_method',
                'desired', 'document_reference_id', 'source', 'entered_by', )
            }),
        )
    fieldsets = add_fieldsets + (
#         ( 'Order Information', {
#             'description' : 'Design Order tracking information',
#             'fields': ( 'customer', 'received', 'project_name', 'design_type', 
#                 'color_views', 'elevations', 'price_report', 'addl_notification_method',
#                 'desired', 'document_reference_id', 'source', 'entered_by', )
#             }),
        ( 'Cabinetry Selections', {
            'classes' : ['collapse'],
            'description' : None,
            'fields' : ( 'cabinet_manufacturer', 'cabinet_door_style', 'cabinet_wood',
                'cabinet_stain', 'cabinet_finish', 'cabinet_finish_options', 'cabinetry_notes' )
            }),
        ( 'Door & Drawer Hardware Selections', {
            'classes' : ['collapse'],
            'description' : None,
            'fields' : ( 'include_hardware', 'door_hardware', 'drawer_hardware' )
            }),
        ( 'Moulding Selections', {
            'classes' : ['collapse'],
            'description' : None,
            'fields' : ( 'ceiling_height', 'crown_mouldings', 'skirt_mouldings',
                'soffits', 'soffit_height', 'soffit_width', 'soffit_depth' )
            }),
        ( 'Cabinet Box Dimensions', {
            'classes' : ['collapse'],
            'description' : None,
            'fields' : ( 'stacked_staggered', 'wall_cabinet_height', 'vanity_cabinet_height',
                'vanity_cabinet_depth' )
            }),            
        ( 'Corner Cabinet Selections', {
            'classes' : ['collapse'],
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
        ( 'Interior Options', {
            'classes' : ['collapse'],
            'description' : None,
            'fields' : ( 'lazy_susan', 'slide_out_trays', 'waste_bin', 'wine_rack', 'plate_rack', 'appliance_garage' )
            }),
        ( 'Miscellaneous', {
            'classes' : ['collapse'],
            'description' : None,
            'fields' : ( 'corbels_brackets', 'valance', 'legs_feet', 'glass_doors', 'range_hood', 'posts' )
            }),
    )                      
    
    def add_view(self, request):
    
        if request.method == 'POST':
            form = CreateOrderForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                msg = _('The %(name)s "%(obj)s" was added successfully.') % {'name': 'user', 'obj': new_user}
                self.log_addition(request, new_user)
                if "_addanother" in request.POST:
                    request.user.message_set.create(message=msg)
                    return HttpResponseRedirect(request.path)
                elif '_popup' in request.REQUEST:
                    return self.response_add(request, new_user)
                else:
                    request.user.message_set.create(message=msg + ' ' + ugettext("You may edit it again below."))
                    return HttpResponseRedirect('../%s/' % new_user.id)
        else:
            form = CreateOrderForm()

        adminForm = admin.helpers.AdminForm(form, list(self.add_fieldsets), self.prepopulated_fields)
            
        return render_to_response('admin/change_form.html', {
            'title': _('New Order'),
            'form': form,
            'adminform': adminForm,
            'is_popup': '_popup' in request.REQUEST,
            'add': True,
            'change': False,
            'has_add_permission': True,
            'has_delete_permission': False,
            'has_change_permission': True,
            'has_file_field': False,
            'has_absolute_url': False,
            'auto_populated_fields': (),
            'opts': self.model._meta,
            'save_as': False,
            'root_path': self.admin_site.root_path,
            'app_label': self.model._meta.app_label,            
        }, context_instance=template.RequestContext(request))
        

admin.site.register(DesignOrder, DesignOrderAdmin)
# admin.site.register(OrderAppliance)
# admin.site.register(OrderAttachment)
# admin.site.register(OrderNotes)
# admin.site.register(DealerOrganization)

# admin.site.register(Transaction)
# admin.site.register(UserProfile)


