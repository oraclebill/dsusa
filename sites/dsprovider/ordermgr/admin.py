from django.contrib import admin
import models


class DesignOrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'source', 'status', 'arrived')


# admin.site.register(models.DesignOrder, DesignOrderAdmin)
admin.site.register(models.KitchenDesignRequest, DesignOrderAdmin)
admin.site.register(models.DesignOrderEvent)
