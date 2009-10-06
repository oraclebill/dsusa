from django.contrib import admin

from models import DesignOrder, DesignOrderEvent, KitchenDesignRequest

admin.site.register(DesignOrder)
admin.site.register(DesignOrderEvent)
admin.site.register(KitchenDesignRequest)
