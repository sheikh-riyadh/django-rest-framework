from django.urls import path, include
from product.views import ProductViewSet, ReviewViewSet
from rest_framework_nested import routers
from order.views import CartViewSet

router = routers.DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('review', ReviewViewSet, basename='product-review')
router.register('carts', CartViewSet, basename='carts')


product_router = routers.NestedDefaultRouter(router, 'products', lookup='product')
product_router.register('review', ReviewViewSet, basename='product-review')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls))
]
