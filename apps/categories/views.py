from rest_framework import generics
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from .models import Category
from .serializers import CategorySerializer, CategoryDetailSerializer
from apps.products.serializers import ProductListSerializer
from apps.products.models import Product


class CategoryListView(generics.ListAPIView):
    """
    Barcha faol kategoriyalar (faqat root kategoriyalar, children bilan).
    """
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        return Category.objects.filter(
            is_active=True, parent__isnull=True
        ).prefetch_related('children')


class CategoryDetailView(generics.RetrieveAPIView):
    """
    Bitta kategoriya (slug bo'yicha).
    """
    serializer_class = CategoryDetailSerializer
    permission_classes = [AllowAny]
    queryset = Category.objects.filter(is_active=True)
    lookup_field = 'slug'


class CategoryProductsView(generics.ListAPIView):
    """
    Berilgan kategoriya va uning barcha ichki kategoriyalaridagi aktiv mahsulotlar.
    """
    serializer_class = ProductListSerializer
    permission_classes = [AllowAny]

    def get_queryset(self):
        slug = self.kwargs['slug']
        category = get_object_or_404(Category, slug=slug, is_active=True)

        # Kategoriya va uning barcha ichki kategoriyalari
        category_ids = [category.id] + [c.id for c in category.get_all_children()]

        return Product.objects.filter(
            category_id__in=category_ids,
            status='aktiv'
        ).select_related('category', 'seller').prefetch_related('images')
