from django.contrib import admin
from services.models import Item, Category, Location


class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "active", "created", "last_updated", "location")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "location")

admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
