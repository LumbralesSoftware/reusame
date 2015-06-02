from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import permissions
from .permissions import IsOwnerOrReadOnly
from services.models import Item
from services.serializers import ItemSerializer

import geopy
from geopy.distance import vincenty as VincentyDistance

SEARCH_RADIUS = 10 # in KMs
COMPASS_BEARING = {
    'NORTH': 0,
    'EAST': 90,
    'SOUTH': 180,
    'WEST': 270,
}

def translate_point(point, bearing):
    origin = geopy.Point(point['latitude'], point['longitude'])
    destination = VincentyDistance(
        kilometers=SEARCH_RADIUS
    ).destination(origin, bearing)
    return destination

def make_bounding_box(point, radius):
    max_lat = translate_point(
        point,
        COMPASS_BEARING['NORTH']
    ).latitude
    min_lat = translate_point(
        point,
        COMPASS_BEARING['SOUTH']
    ).latitude
    max_long = translate_point(
        point,
        COMPASS_BEARING['EAST']
    ).longitude
    min_long = translate_point(
        point,
        COMPASS_BEARING['WEST']
    ).longitude
    # Fetch locations within the bounding box
    items = Item.objects.filter(
        location__lat_position__gt=min_lat,
        location__lat_position__lt=max_lat,
        location__long_position__gt=min_long,
        location__long_position__lt=max_long,
    )
    return items

def vincenty_filter(point, locations, radius):
    nearby_locations = []
    for location in locations:
        distance = vincenty(
            (point['latitude'], point['longitude']),
            (location.latitude, location.longitude)
        ).kilometers
        if distance <= SEARCH_RADIUS:
            nearby_locations.append(location)
    return nearby_locations

def find_nearby_locations(point):
    bb_locations = make_bounding_box(point, SEARCH_RADIUS)
    return vincenty_filter(point, bb_locations, SEARCH_RADIUS)


class ItemViewSet(viewsets.ModelViewSet):
    serializer_class = ItemSerializer
    model = Item
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly,)

    def get_queryset(self):
        """
        Optionally restricts the returned nodes to a given location
        by filtering against a `lat`, `lon` query parameter in the URL.
        """
        queryset = Item.objects.all()
        lat = self.request.QUERY_PARAMS.get('lat', None)
        lon = self.request.QUERY_PARAMS.get('lon', None)
        if lat is not None and lon is not None:
            queryset = make_bounding_box(
                {"latitude": lat, "longitude": lon},
                SEARCH_RADIUS
            )
            print queryset.count()
            # If not 1 fall back to all items
            if queryset.count() <= 1:
                 queryset = Item.objects.all()
        return queryset
