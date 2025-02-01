from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView

from . import models
from . import serializers


class CategoryList(ListCreateAPIView):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()


@api_view(['GET', 'PATCH','DELETE'])
def category_detail(request, pk):
    category = get_object_or_404(models.Category, pk=pk)

    if request.method == 'GET':
        serializer = serializers.CategorySerializer(category)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = serializers.CategorySerializer(category ,data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        category.delete()
        return Response('Category were deleted' ,status=status.HTTP_202_ACCEPTED)
        


@api_view(['GET', 'POST'])
def product_list(request):
    if request.method == 'GET':
        queryset = models.Product.objects.select_related('category').prefetch_related('available_colors', 'available_size').all()
        serializer = serializers.ProductSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'POST':
        serializer = serializers.ProductSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
@api_view(['GET', 'PATCH', 'DELETE'])
def product_detail(request, pk):
    product = get_object_or_404(models.Product, pk=pk)

    if request.method == 'GET':
        serializer = serializers.ProductSerializer(product)
        return Response(serializer.data)
    elif request.method == 'PATCH':
        serializer = serializers.ProductSerializer(data= request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'DELETE':
        product.delete()
        return Response(status=status.HTTP_200_OK)
    
    