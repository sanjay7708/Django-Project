from django.shortcuts import render
from . models import (
    Category,Product,Variation,ProductImage,
    Cart,cartItem,Address,Order,OrderItem,ContactForm)
from .serializers import (
    CartItemSerializer,CartSerializer,ProductSerializer,
    AddressSerializer,OrderSerializer,OrderItemSerializer,ContactSerializer)
from rest_framework import viewsets,permissions
from django.db.models import Q

# Create your views here.


class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all().select_related("category").prefetch_related("variations","images")
    serializer_class=ProductSerializer
    permission_classes=[permissions.IsAuthenticated]
    lookup_field="slug"


    def get_queryset(self):
        queryset=super().get_queryset()
        query = self.request.query_params.get("q")
        if query:
            # 🔍 Search across multiple fields for better user experience
            queryset = queryset.filter(
                Q(short_name__icontains=query) |
                Q(description__icontains=query) |
                Q(category__name__icontains=query)
            )

        return queryset
class CartViewSet(viewsets.ModelViewSet):
    serializer_class=CartSerializer
    permission_classes=[permissions.IsAuthenticated]


    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class CartItemViewSet(viewsets.ModelViewSet):
    serializer_class=CartItemSerializer
    permission_classes=[permissions.IsAuthenticated]


    def get_queryset(self):
        return cartItem.objects.filter(cart__user=self.request.user)
    def perform_create(self, serializer):
        cart,_=Cart.objects.get_or_create(user=self.request.user)
        product=serializer.validated_data['product']
        variation=serializer.validated_data.get('variation')


        existing_item=cartItem.objects.filter(cart=cart,product=product,variation=variation).first()
        if existing_item:
            existing_item.quantity+=serializer.validated_data.get("quantity",1)
            existing_item.save()
        else:
            serializer.save(cart=cart)
    def perform_update(self, serializer):
        instance=serializer.save()
        if instance.quantity<=0:
            instance.delete()
            
class AddressViewSet(viewsets.ModelViewSet):
    serializer_class=AddressSerializer
    permission_classes=[permissions.IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderViewSet(viewsets.ModelViewSet):
    
    serializer_class=OrderSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class OrderItemViewSet(viewsets.ModelViewSet):
    
    serializer_class=OrderItemSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get_queryset(self):
        return OrderItem.objects.filter(order__user=self.request.user)

    def perform_create(self, serializer):
    
        order = Order.objects.filter(user=self.request.user).first()
        if not order:
            order = Order.objects.create(user=self.request.user)
        serializer.save(order=order)

class ContactView(viewsets.ModelViewSet):
    queryset=ContactForm.objects.all()
    serializer_class=ContactSerializer