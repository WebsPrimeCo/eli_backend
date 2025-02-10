from django.urls import include, path
from rest_framework_nested import routers

from . import views


router = routers.DefaultRouter()
router.register('product', views.ProductViewSet, basename='product')
router.register('categories', views.CategoryViewSet, basename='category')
router.register('carts', views.CartViewSet, basename='cart')

product_router = routers.NestedDefaultRouter(router, 'product', lookup = 'product')
product_router.register('comments', views.CommentViewSet, basename='product-comment')

cart_items_router = routers.NestedDefaultRouter(router, 'carts', lookup= 'cart')
cart_items_router.register('items', views.CartItemViewSet, basename='cart-items')

urlpatterns = router.urls + product_router.urls + cart_items_router.urls

