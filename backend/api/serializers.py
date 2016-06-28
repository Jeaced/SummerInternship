from rest_framework import serializers
from api.models import Item, Component, Order, OrderComposition

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

#class OrderCompositionSerializer(serializers.HyperlinkedModelSerializer):
 #   item_id = serializers.ReadOnlyField(Item.pk)
  #  amount = serializers.IntegerField()
#
 #   class Meta:
  #      model = OrderComposition
   #     fields = ('item', 'amount',)

#class OrderSerializer(serializers.ModelSerializer):
 #   items = OrderCompositionSerializer(source='ordercomposition_set', many=True)
#
 #   class Meta:
  #      model = Order
   #     fields = ('id', 'date', 'total_price', 'payment_method', 'user', 'items')

class ItemAmountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()


class OrderWithItemsSerializer(serializers.Serializer):
   id = serializers.IntegerField()
   date = serializers.DateField()
   total_price = serializers.DecimalField(max_digits=12, decimal_places=2)
   payment_method = serializers.CharField()
   user = serializers.CharField()
   items = serializers.ListField(child=ItemAmountSerializer(many=True))




   
