from django.contrib import admin
from order.models import Cart,CartItem,Order,OrderItem


# Register your models here.
@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['user', 'id']


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ['cart', 'product', 'quantity']


admin.site.register(Order)
admin.site.register(OrderItem)