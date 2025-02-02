from django.urls import path

from . import views

urlpatterns = [
    path('category/', views.CategoryList.as_view(), name= 'category_list'),
    path('category/<int:pk>/', views.CategoryDetail.as_view(), name='category_detail'),
    path('product/', views.ProductList.as_view(), name='product_list'),
    path('product/<int:pk>/', views.ProductDetail.as_view(), name='product_detail')
]
