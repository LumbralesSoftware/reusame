from django.shortcuts import render
from rest_framework import viewsets
from services.models import Item
from services.serializers import ItemSerializer

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
