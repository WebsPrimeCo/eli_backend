from django.shortcuts import get_object_or_404, render
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListCreateAPIView

from . import models
from . import serializers


class CategoryViewSet(ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()

class ProductViewSet(ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.select_related('category').prefetch_related('available_colors', 'available_size').all()

    def get_serializer_context(self):
        return {'request': self.request}
    
class CommentViewSet(ModelViewSet):
    serializer_class = serializers.CommentSerializer
    
    def get_queryset(self):
        product_pk = self.kwargs['product_pk']
        return models.Comment.objects.filter(product_id=product_pk).all()

    def get_serializer_context(self):
        return {
            'request':self.request,
            'product_pk': self.kwargs['product_pk'],
                } 