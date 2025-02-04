from django.urls import include, path
from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.register('product', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')

product_router = routers.NestedDefaultRouter(router, 'product', lookup = 'product')
product_router.register('comments', views.CommentViewSet, basename='product-comment')

urlpatterns = router.urls + product_router.urls

