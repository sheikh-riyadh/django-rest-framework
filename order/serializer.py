from rest_framework import serializers
from order.models import Cart, CartItem,Order,OrderItem
from product.models import Product
from order.services import OrderService


class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price']



class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()
    class Meta:
        model = CartItem
        fields =['product_id', 'quantity']
    
    def save(self, **kwargs):
        cart_id = self.context.get('cart_id')
        product_id = self.validated_data.get('product_id')
        quantity = self.validated_data.get('quantity')

        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity +=quantity
            self.instance = cart_item.save()

        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, product_id=product_id, quantity=quantity)

        return self.instance
    
    def validate_product_id(self, id):
        try:
            Product.objects.get(pk=id)
        except Product.DoesNotExist:
            raise serializers.ValidationError(f'Product with id {id} does not exist.')
        return id
        
  

class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']


class CartItemSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    total_price = serializers.SerializerMethodField(method_name='get_total_price', read_only=True)
    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity', 'total_price']

    def validate(self, attrs):
        cart_id = self.context.get('cart_id')

        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("Cart does not exist")

        return attrs

    def get_total_price(self, items:CartItem):
        return items.product.price * items.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, source='item', read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price', read_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'id', 'items', 'total_price']
        read_only_fields = ['user']

    def get_total_price(self, cart:Cart):
        total = sum(list([item.product.price * item.quantity for item in cart.items.all()]))
        return total
   


class CreateOrderSerializer(serializers.Serializer):
    cart_id = serializers.UUIDField()

    def validate_cart_id(self, cart_id):
        if not Cart.objects.filter(pk=cart_id).exists():
            raise serializers.ValidationError("Cart not found")
        if not CartItem.objects.filter(cart_id=cart_id).exists():
            raise serializers.ValidationError("Cart is empty")
        return cart_id
    

    def create(self, validated_data):
        user_id = self.context.get('user_id')
        cart_id = validated_data.get('cart_id')
        try:
            order = OrderService.create_order(cart_id=cart_id, user_id=user_id)
            return order
        except ValueError as e:
            serializers.ValidationError(str(e))
    
    def to_representation(self, instance):
        return OrderSerializer(instance).data
        
        

class OrderItemsSerializer(serializers.ModelSerializer):
    product = SimpleProductSerializer()
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'product', 'quantity', 'price', 'total_price']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemsSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'status', 'total_price', 'created_at', 'items']



