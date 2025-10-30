from django.urls import path
from product import views

urlpatterns = [
    path('categories/', views.Categories_view.as_view(), name='categories'),
    path('category/<int:pk>/', views.CategoryView.as_view(), name='category')

]
