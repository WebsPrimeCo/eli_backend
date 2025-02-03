from django.urls import include, path
from rest_framework.routers import SimpleRouter, DefaultRouter

from . import views


router = DefaultRouter()
router.register('product', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')

urlpatterns = [
    path('', include(router.urls))
]

