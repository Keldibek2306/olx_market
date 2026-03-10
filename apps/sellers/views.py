from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

from .models import SellerProfile
from .serializers import (
    SellerProfileSerializer, SellerProfileCreateSerializer, SellerProfileUpdateSerializer
)
from .permissions import IsSeller, IsSellerOwner
from apps.products.serializers import ProductListSerializer
from apps.products.models import Product


class SellerProfileCreateView(generics.CreateAPIView):
    """
    Sotuvchi profili yaratish (faqat seller role uchun).
    """
    serializer_class = SellerProfileCreateSerializer
    permission_classes = [IsSeller]


class SellerProfileDetailView(generics.RetrieveUpdateAPIView):
    """
    O'z sotuvchi profilini ko'rish va tahrirlash.
    """
    permission_classes = [IsSeller, IsSellerOwner]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return SellerProfileUpdateSerializer
        return SellerProfileSerializer

    def get_object(self):
        return get_object_or_404(SellerProfile, user=self.request.user)


class PublicSellerDetailView(generics.RetrieveAPIView):
    """
    Ommaviy sotuvchi ma'lumotlari (barcha foydalanuvchilar ko'rishi mumkin).
    """
    serializer_class = SellerProfileSerializer
    permission_classes = [AllowAny]
    queryset = SellerProfile.objects.select_related('user')
    lookup_field = 'user_id'
    lookup_url_kwarg = 'seller_id'


class SellerProductsView(generics.ListAPIView):
    """
    Sotuvchining barcha aktiv mahsulotlari.
    """
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        seller_id = self.kwargs['seller_id']
        seller_profile = get_object_or_404(SellerProfile, user_id=seller_id)
        return Product.objects.filter(
            seller=seller_profile.user,
            status='aktiv'
        ).select_related('category', 'seller').prefetch_related('images')
