from rest_framework import serializers
from .models import CartItem
from products.serializers import ProductSerializer

class CartItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source='product', read_only=True)
    
    class Meta:
        model = CartItem
        fields = ('id', 'product', 'product_details', 'quantity', 'subtotal')
        read_only_fields = ('id', 'subtotal')
