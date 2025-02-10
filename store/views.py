from django.shortcuts import get_object_or_404, render
from rest_framework.viewsets import ModelViewSet
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins


from . import models
from . import serializers
from .pagination import DefaultPaginations

class CategoryViewSet(ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()

class ProductViewSet(ModelViewSet):
    serializer_class = serializers.ProductSerializer
    queryset = models.Product.objects.select_related('category').prefetch_related('available_colors', 'available_size').all()
    filter_backends = [SearchFilter,DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['category_id']
    ordering_fields = ['title', 'price']
    search_fields = ['title',]
    pagination_class = DefaultPaginations

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
    

class CartViewSet(ModelViewSet):
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_queryset(self):
        cart_pk = self.kwargs['cart_pk']
        return models.CartItem.objects.select_related('product').filter(cart_id=cart_pk).all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return serializers.UpdateCartItemSerializer

    def get_serializer_context(self):
        return {'cart_pk': self.kwargs['cart_pk']}  