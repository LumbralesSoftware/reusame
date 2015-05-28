from rest_framework import serializers
from services.models import Item, Category, Location

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ('location', 'long_position', 'lat_position')

class ItemSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    category = serializers.StringRelatedField()
    class Meta:
        model = Item
        fields = ('id', 'name', 'text', 'image', 'category', 'location', 'active')

