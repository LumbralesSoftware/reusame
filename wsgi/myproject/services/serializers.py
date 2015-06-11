from rest_framework import serializers
from services.models import Item, Category, Location
from django.shortcuts import get_object_or_404

from .utils import get_coords, get_address

class CategoryField(serializers.RelatedField):

    def to_representation(self, value):
        return value.name

    def to_internal_value(self, value):
        category = get_object_or_404(Category, name=value)
        return category

class LocationSerializer(serializers.ModelSerializer):
    location = serializers.CharField(allow_blank=True, required=False)
    long_position = serializers.CharField(allow_blank=True, required=False)
    lat_position = serializers.CharField(allow_blank=True, required=False)
    class Meta:
        model = Location
        fields = ('location', 'long_position', 'lat_position')

    def validate(self, location):
        if not 'location' in location or (not location['location'] and not location['long_position'] and not location['lat_position']):
            raise serializers.ValidationError('You must provide either location address or lat/long coordinates.')
        return super(LocationSerializer, self).validate(location)

class ItemSerializer(serializers.ModelSerializer):
    location = LocationSerializer()
    category = CategoryField(queryset=Category.objects.all())
    owner = serializers.ReadOnlyField(source='owner.username')
    created = serializers.DateTimeField(read_only=True)
    expires_on = serializers.DateTimeField() #format="%d %b %Y %H:%M:%S"
    class Meta:
        model = Item
        fields = ('id', 'name', 'description', 'image', 'category', 'location', 'owner', 'created', 'expires_on')

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request is not None:
            user = request.user
        else:
            return false

        address = validated_data['location']['location']
        lat = validated_data['location']['lat_position']
        lon = validated_data['location']['long_position']
        if not address:
            address = get_address(lat, lon)
        elif not lat or not lon:
            lat, lon = get_coords(address)

        location = Location.objects.create(
            lat_position=lat,
            long_position=lon,
            location=address,
            )
        location.save()

        # Create the item instance
        item = Item.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            image=validated_data['image'],
            category=validated_data['category'],
            location=location,
            owner=user
        )

        return item
