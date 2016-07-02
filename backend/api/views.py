from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from api.permissions import IsManagerOrReadOnly, IsSuperuser
from api.serializers import ItemSerializer, ComponentSerializer, OrderWithItemsSerializer
from api.models import Item, Component, Order, OrderComposition
from rest_framework import status, permissions
from django.http import Http404
from api.orders import OrderWithItems, ItemAmount

# Create your views here.
class ItemList(APIView):
	permission_classes = (IsManagerOrReadOnly,)

	def get(self, request, format=None):
		items = Item.objects.all()
		serializer = ItemSerializer(items, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = ItemSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetail(APIView):
	permission_classes = (IsManagerOrReadOnly,)

	def get_object(self, pk):
		try:
			return Item.objects.get(pk=pk)
		except Item.DoesNotExist:
			raise Http404

	def get(self, request, pk, format=None):
		item = self.get_object(pk)
		serializer = ItemSerializer(item)
		return Response(serializer.data)

	def put(self, request, pk, format=None):
		item = self.get_object(pk)
		serializer = ItemSerializer(dish, data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)	

	def delete(self, request, pk, format=None):
		item = self.get_object(pk)
		item.delete()
		return Response(status=status.HTTP_204_NO_CONTENT)		


class ComponentList(APIView):
    permission_classes = (IsManagerOrReadOnly,)
    
    def get(self, request, format=None):
        components = Component.objects.all()
        serializer = ComponentSerializer(components, many=True)

        return Response(serializer.data)
    
    def post(self, request, format=None):
        serializer = ComponentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ComponentDetail(APIView):
    permission_classes = (IsManagerOrReadOnly,)

    def get_object(self, pk):
        try:
            return Component.objects.get(pk=pk)
        except Component.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        component = self.get_object(pk)
        serializer = ComponentSerializer(component)

        return Response(serializer.data)

    def put(self, request, pk, format=None):
        component = self.get_object(pk)
        serializer = ComponentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk, format=None):
        component = self.get_object(pk)
        component.delete()

        return Response(status=status.HTTP_204_NO_CONTENT)


class OrderList(APIView):
    permission_classes = (IsManagerOrReadOnly,)

    def get(self, request, format=None):
        orders = Order.objects.all()
        order_contents = OrderComposition.objects.all()
        orders_with_items = list()
        for order in orders:
            contents = get_contents_by_id(order_contents, order.id)
            item_amount = list()
            for content in contents:
                item_amount.append(ItemAmount(content.item_id.id, content.amount))

            orders_with_items.append(OrderWithItems(order, item_amount))
            
        serializer = OrderWithItemsSerializer(orders_with_items, many=True)

        return Response(serializer.data)
    
    #def post(self, request, format=None):
     #   serializer = OrderSerializer(data=request.data)
      #  if serializer.is_valid():
       #     serializer.save()
       #     return Response(serializer.data, status=status.HTTP_201_CREATED)
        
       # return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def get_contents_by_id(order_contents, id):
    contents = list()
    for order_content in order_contents:
        if order_content.order_id.id == id:
            contents.append(order_content)

    return contents

