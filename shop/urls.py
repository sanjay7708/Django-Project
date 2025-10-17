from django.urls import path,include
from rest_framework.routers import DefaultRouter
from . views import ProductViewSet,CartViewSet,CartItemViewSet,AddressViewSet,OrderViewSet,OrderItemViewSet,ContactView

router=DefaultRouter()
router.register(r'product',ProductViewSet)
router.register(r'cart',CartViewSet,basename='cart')
router.register(r'cartitem',CartItemViewSet,basename='cartitem')
router.register(r"address",AddressViewSet,basename='address')
router.register('order',OrderViewSet,basename='order')
router.register('orderitem',OrderItemViewSet,basename='orderitem')
router.register('contact',ContactView)

urlpatterns=[
    path('',include(router.urls)),
]

