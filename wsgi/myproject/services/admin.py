from django.contrib import admin
from services.models import Item, Category, Location, UserRating, UserRequest


class ItemAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "owner", "active", "created", "last_updated", "location")

class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name")

class LocationAdmin(admin.ModelAdmin):
    list_display = ("id", "location")

class UserRatingsAdmin(admin.ModelAdmin):
    list_display = ("id", "voted_user", "voting_user", "punctuation")

class UserRequestsAdmin(admin.ModelAdmin):
    list_display = ("id", "requester", "item", "created")

admin.site.register(Item, ItemAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Location, LocationAdmin)
admin.site.register(UserRating, UserRatingsAdmin)
admin.site.register(UserRequest, UserRequestsAdmin)
