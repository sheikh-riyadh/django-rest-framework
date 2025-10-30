from django.urls import path
from product import views

urlpatterns = [
    path('products/', views.GenericProductView.as_view(), name='products'),
    path('product/<int:pk>/', views.view_specific_product, name='product')
]
