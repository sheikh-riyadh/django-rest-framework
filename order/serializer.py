from rest_framework import serializers
from order.models import Cart, CartItem
from product.models import Product


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price', read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def get_total_price(self, items:CartItem):
        return items.product.price * items.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, source='item')
    total_price = serializers.SerializerMethodField(method_name='get_total_price')

    class Meta:
        model = Cart
        fields = ['user', 'id', 'items', 'total_price']

    
    def get_total_price(self, cart:Cart):
        total = sum(list([item.product.price * item.quantity for item in cart.item.all()]))
        return total
   



