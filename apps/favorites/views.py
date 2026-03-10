from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import F

from .models import Favorite
from .serializers import FavoriteSerializer, FavoriteCreateSerializer
from apps.products.models import Product


class FavoriteListCreateView(generics.ListCreateAPIView):
    """
    GET: O'z sevimlilarini ko'rish
    POST: Sevimlilarga qo'shish
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return FavoriteCreateSerializer
        return FavoriteSerializer

    def get_queryset(self):
        return Favorite.objects.filter(
            user=self.request.user
        ).select_related('product__category', 'product__seller').prefetch_related('product__images')


class FavoriteDeleteView(generics.DestroyAPIView):
    """
    DELETE: Sevimlilardan olib tashlash.
    """
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    def perform_destroy(self, instance):
        # favorite_count ni kamaytirish
        Product.objects.filter(pk=instance.product_id).update(
            favorite_count=F('favorite_count') - 1
        )
        instance.delete()
