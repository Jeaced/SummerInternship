from rest_framework import serializers

from api.models import Item, Component, OrderDetail, OrderContent, ItemHistory, ComponentHistory
from api.orders import Order, get_order_detail, get_order_contents


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

class ItemHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ItemHistory
        field = ('date',
                 'item',
                 'amount')

class ComponentHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ComponentHistory
        field = ('date',
                 'component',
                 'amount')                          

class ItemAmountSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.IntegerField()


class OrderSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    date = serializers.DateTimeField()
    total_price = serializers.DecimalField(max_digits=12, decimal_places=2)
    payment_method = serializers.CharField()
    user = serializers.IntegerField()
    items = serializers.ListField(child=ItemAmountSerializer())

    def create(self, validated_data):
        validated_data['order_id'] = validated_data.pop('id')
        validated_data['user_id'] = validated_data.pop('user')
        order = Order(**validated_data)

        order_detail = get_order_detail(order)
        order_detail.save()
        order_contents = get_order_contents(order)
        for order_content in order_contents:
            order_content.save()

        return order