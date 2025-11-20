from django.urls import path, include
from product.views import ProductViewSet, ReviewViewSet,CategoryViewSet
from rest_framework_nested import routers
from order.views import CartViewSet,CartItemViewSet

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('review', ReviewViewSet, basename='product-review')
router.register('categories', CategoryViewSet, basename='categories')
router.register('carts', CartViewSet, basename='carts')



# Product Nested Router
product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('review', ReviewViewSet, basename='product-review')

# Cart Nested Router
cart_router = routers.NestedDefaultRouter(router, 'carts', lookup='cart')
cart_router.register('items', CartItemViewSet, basename='cart-item')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(cart_router.urls)),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
