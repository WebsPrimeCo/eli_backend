from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view
from rest_framework.response import Response

from . import models
from . import serializers


@api_view(['GET'])
def category_view(request):
    queryset = models.Category.objects.all()
    serializer = serializers.CategorySerializer(queryset, many=True)
    return Response(serializer.data)


@api_view()
def category_detail(request, pk):
    category = get_object_or_404(models.Category, pk=pk)
    serializer = serializers.CategorySerializer(category )
    return Response(serializer.data)


@api_view()
def product_list(request):
    queryset = models.Product.objects.select_related('category').prefetch_related('available_colors', 'available_size').all()
    serializer = serializers.ProductSerializer(queryset, many=True)
    return Response(serializer.data)
