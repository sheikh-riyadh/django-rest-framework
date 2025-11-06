from rest_framework import serializers
from order.models import Cart, CartItem
from product.models import Product


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

    def get_total_price(self, items:CartItem):
        return items.product.price * items.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, source='item', read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price', read_only=True)

    class Meta:
        model = Cart
        fields = ['user', 'id', 'items', 'total_price']

    
    def get_total_price(self, cart:Cart):
        total = sum(list([item.product.price * item.quantity for item in cart.item.all()]))
        return total
   



