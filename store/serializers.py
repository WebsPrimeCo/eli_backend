from rest_framework import serializers
from django.utils.text import slugify

from . import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id','title', 'description']

class DiscountSerializer(serializers.ModelSerializer):
    model = models.Discount
    fields = ['discount', 'description']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = [
            'id',
            'category',
            'image_1',
            'image_2',
            'image_3',
            'title',
            'inventory',
            'descriptions',
            'price',
            'available_colors',
            'available_size'
        ]
    def create(self, validated_data):
        product = models.Product(**validated_data)
        product.slug = slugify(product.name)
        product.save()
        return product

