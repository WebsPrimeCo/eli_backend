from rest_framework import serializers
from django.utils.text import slugify

from . import models

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id','title', 'description']


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
    
class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = models.Comment
        fields = ['id', 'product', 'body', 'user']

    def create(self, validated_data):
        product_id = self.context['product_pk']
        user = self.context['request'].user
        return models.Comment.objects.create(user=user, **validated_data)

