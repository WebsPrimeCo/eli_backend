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
    
class ProductCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['id', 'image_1', 'title', 'price', 'available_colors', 'available_size']
    
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductCartItemSerializer()
    item_total = serializers.SerializerMethodField()
    class Meta:
        model = models.CartItems
        fields = ['id', 'product', 'quantity', 'item_total']

    def get_item_total(self, cart_item):
        return cart_item.quantity * cart_item.product.price
    
class AddCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CartItems
        fields = ['id', 'product', 'quantity']

    def create(self, validated_data):
        cart_id = self.context['cart_pk']
        product = validated_data.get('product')
        quantity = validated_data.get('quantity')

        try:
            cart_item= models.CartItems.objects.get(cart_id=cart_id, product_id = product.id)
            cart_item.quantity += quantity
            cart_item.save()
        except models.CartItems.DoesNotExist:
            cart_item = models.CartItems.objects.create(cart_id=cart_id, **validated_data)
        
        self.instance = cart_item
        return cart_item



class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many= True)
    total_price = serializers.SerializerMethodField()
    class Meta:
        model = models.Cart
        fields = ['id', 'items', 'total_price']
        read_only_fields = ['id']

    def get_total_price(self, cart):
        return sum([item.quantity * item.product.price for item in cart.items.all()])

        # ff332a86-c70a-487a-9450-4f92fff8c167
