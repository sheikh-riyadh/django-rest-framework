from django.shortcuts import render
from rest_framework.viewsets import GenericViewSet,ModelViewSet
from rest_framework.mixins import RetrieveModelMixin,UpdateModelMixin,DestroyModelMixin,CreateModelMixin
from order.models import Cart, CartItem
from order.serializer import CartSerializer, CartItemSerializer


# Create your views here.
class CartViewSet(GenericViewSet, CreateModelMixin, RetrieveModelMixin):
    queryset = Cart.objects.prefetch_related('item').all()
    serializer_class = CartSerializer


# class CartItemViewSet(ModelViewSet):
#     queryset = CartItem.objects.all
#     serializer_class = CartItemSerializer(many=True)

