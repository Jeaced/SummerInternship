from rest_framework import serializers
from api.models import Item
from api.models import Component

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        field = ('id', 
                 'title', 
                 'image_link', 
                 'created', 
                 'units', 
                 'price_per_unit')


class ComponentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Component
        field = ('id',
                 'title',
                 'created',
                 'units',
                 'price_per_unit')



                 
