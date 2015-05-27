from rest_framework import serializers
from services.models import Item, Category, Location

# Serializers define the API representation.
class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ('id', 'name', 'text', 'image', 'category', 'location', 'active')

