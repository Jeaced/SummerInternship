from rest_framework.views import APIView
from rest_framework.response import Response
from api.permissions import IsManagerOrReadOnly
from api.serializers import ItemSerializer, ComponentSerializer, OrderSerializer, ItemHistorySerializer, ComponentHistorySerializer
from api.models import Item, Component, ItemHistory, ComponentHistory, Composition
from rest_framework import status
from django.http import Http404
from api.orders import Order, ItemAmount, get_orders, get_order, delete_order
from django.db.models import F


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
        serializer = ItemSerializer(item, data=request.data)
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
        serializer = OrderSerializer(get_orders(),
                                     many=True)

        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            date = serializer.validated_data.get("date")
            order_items = serializer.validated_data.get("items")
            for i in order_items:
                item = Item.objects.get(pk=i.get("id"))
                if ItemHistory.objects.filter(date=date, item=item).exists():
                    item_sold = ItemHistory.objects.get(date=date, item=item)
                    item_sold.amount = F('amount') + i.get("amount")
                    item_sold.save()
                else:
                    item_sold = ItemHistory.objects.create(date=date, item=item, amount=i.get("amount"))
                if Composition.objects.filter(item=item).exists():
                    item_components = list()
                    queryset = Composition.objects.filter(item=item)
                    for entry in queryset:
                        item_components.append((entry.component, entry.amount),)
                    for component in item_components:
                        if ComponentHistory.objects.filter(date=date, component=component[0]).exists():
                            component_spent = ComponentHistory.objects.get(date=date, component=component[0])
                            component_spent.amount = F('amount') + (component[1] * i.get("amount"))
                            component_spent.save()
                        else:
                            component_spent = ComponentHistory.objects.create(date=date, component=component[0], amount=(component[1]*i.get("amount")))
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderDetail(APIView):

    permission_classes = (IsManagerOrReadOnly,)

    def get(self, request, pk, format=None):
        try:
            order = get_order(pk)
        except Exception:
            raise Http404
        serializer = OrderSerializer(order)

        return Response(serializer.data)

    def delete(self, request, pk, format=None):
        order = get_order(pk)
        delete_order(order)

        return Response(status=status.HTTP_204_NO_CONTENT)

class ItemHistoryList(APIView):

    permission_classes = (IsManagerOrReadOnly,)

    def get(self, request, format=None):
        items = ItemHistory.objects.all()
        serializer = ItemHistorySerializer(items, many=True)
        return Response(serializer.data)

class ComponentHistoryList(APIView):

    permission_classes = (IsManagerOrReadOnly,)

    def get(self, request, format=None):
        components = ComponentHistory.objects.all()
        serializer = ComponentHistorySerializer(components, many=True)
        return Response(serializer.data) 