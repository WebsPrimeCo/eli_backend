from rest_framework import serializers

from . import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['title', 'description']

class DiscountSerializer(serializers.ModelSerializer):
    model = models.Discount
    fields = ['discount', 'description']

class ProductSerializer(serializers.ModelSerializer):
    model = models.Product
    fields = [
        'category',
        'image_1',
        'image_2',
        'image_3',
        'title',
        'slug',
        'available_colors',
        'available_size',
        'inventory',
        'descriptions',
        'price',
    ]

