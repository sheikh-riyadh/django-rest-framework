from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.mixins import RetrieveModelMixin,DestroyModelMixin,CreateModelMixin
from order.models import Cart, CartItem
from order.serializer import CartSerializer, CartItemSerializer,AddCartItemSerializer,UpdateCartItemSerializer
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class CartViewSet(CreateModelMixin, RetrieveModelMixin, DestroyModelMixin, GenericViewSet):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.prefetch_related('item').filter(user=self.request.user).all()


class CartItemViewSet(ModelViewSet):
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
       items = CartItem.objects.filter(cart_id=self.kwargs.get('cart_pk')).all()
       return items

