from django.contrib import admin
import models


class DesignPackageInline(admin.TabularInline):
    model = models.DesignPackage
    extra = 0
    
class DesignOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'status', 'arrived')
    inlines = [ DesignPackageInline, ]

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', )

# admin.site.register(models.DesignOrder, DesignOrderAdmin)
admin.site.register(models.KitchenDesignRequest, DesignOrderAdmin)
admin.site.register(models.DesignPackage)
admin.site.register(models.DesignOrderEvent)
admin.site.register(models.UserProfile, UserProfileAdmin)
