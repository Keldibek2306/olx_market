from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Q

from .models import Order
from .serializers import (
    OrderListSerializer, OrderDetailSerializer,
    OrderCreateSerializer, OrderUpdateSerializer
)


class OrderListCreateView(generics.ListCreateAPIView):
    
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return OrderCreateSerializer
        return OrderListSerializer

    def get_queryset(self):
        user = self.request.user
        role = self.request.query_params.get('role', 'buyer')

        if role == 'seller':
            return Order.objects.filter(seller=user).select_related(
                'product', 'buyer', 'seller'
            ).prefetch_related('product__images')
        else:
            return Order.objects.filter(buyer=user).select_related(
                'product', 'buyer', 'seller'
            ).prefetch_related('product__images')


class OrderDetailView(generics.RetrieveUpdateAPIView):
    
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return OrderUpdateSerializer
        return OrderDetailSerializer

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(
            Q(buyer=user) | Q(seller=user)
        ).select_related('product', 'buyer', 'seller')
