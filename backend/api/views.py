from django.shortcuts import render
from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from api.permissions import IsManagerOrReadOnly, IsSuperuser
from api.serializers import ItemSerializer
from api.models import Item
from rest_framework import status, permissions

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