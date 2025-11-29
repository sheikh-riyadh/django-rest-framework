from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.mixins import RetrieveModelMixin,DestroyModelMixin,CreateModelMixin
from order.models import Cart, CartItem, Order, OrderItem
from order.serializer import CartSerializer, CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer, OrderSerializer, CreateOrderSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404

# Create your views here.
class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        if Cart.objects.filter(user=self.request.user).exists():
            raise ValidationError({
                'message': 'Cart already exists',
            })

        serializer.save(user=self.request.user)
        

    def get_queryset(self):
        return Cart.objects.prefetch_related('items__product').filter(user=self.request.user).all()


class CartItemViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    http_method_names =['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        else:
            return CartItemSerializer
    
    def get_serializer_context(self):
       context ={
           'cart_id': self.kwargs.get('cart_pk')
       }
       return context

    def get_queryset(self):
       items = CartItem.objects.select_related('product').filter(cart_id=self.kwargs.get('cart_pk')).all()
       return items
    
    def perform_create(self, serializer):
        cart_id = self.kwargs.get("cart_pk")

        # 1) Cart exists?
        cart = get_object_or_404(Cart, id=cart_id)

        # 2) Cart owner check
        if cart.user != self.request.user:
            raise ValidationError("You cannot add items to another user's cart")

        # 3) Save FK properly
        serializer.save(cart=cart)


class OrderViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == "POST":
            return CreateOrderSerializer
        return OrderSerializer
    
    def get_serializer_context(self):
        return {
            'user_id':self.request.user.id
        }

    def get_queryset(self):
        if self.request.user.is_staff:
            Order.objects.prefetch_related('items__product').all()
        return Order.objects.prefetch_related('items__product').filter(user=self.request.user)
        
    