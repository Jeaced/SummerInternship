from rest_framework import serializers
from api.models import Item

class ItemSerializer(serializers.ModelSerializer):
	class Meta:
		model = Item
		field = ('id', 'title', 'image_link', 'created', 'units', 'price_per_unit')