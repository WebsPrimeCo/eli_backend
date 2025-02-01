from django.urls import path

from . import views

urlpatterns = [
    path('category/', views.category_list, name= 'category_list'),
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    path('product/', views.product_list, name='product_list'),
    path('product/<int:pk>/', views.product_detail, name='product_detail')
]
