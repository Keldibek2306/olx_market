from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404

from .models import Product, ProductImage
from .serializers import (
    ProductListSerializer, ProductDetailSerializer,
    ProductCreateSerializer, ProductUpdateSerializer
)
from .permissions import IsSellerOrReadOnly, IsProductOwner
from .filters import ProductFilter


class ProductListCreateView(generics.ListCreateAPIView):
    """
    GET: Barcha aktiv mahsulotlar (filter, search, pagination)
    POST: Yangi e'lon yaratish (faqat seller)
    """
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']
    ordering_fields = ['created_at', 'price', 'view_count', 'favorite_count']
    ordering = ['-created_at']

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated(), IsSellerOrReadOnly()]
        return [AllowAny()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ProductCreateSerializer
        return ProductListSerializer

    def get_queryset(self):
        return Product.objects.filter(
            status='aktiv'
        ).select_related('category', 'seller').prefetch_related('images')


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET: Bitta mahsulot (view_count +1)
    PUT/PATCH: Tahrirlash (faqat egasi)
    DELETE: O'chirish (faqat egasi)
    """
    queryset = Product.objects.select_related('category', 'seller').prefetch_related('images')

    def get_permissions(self):
        if self.request.method == 'GET':
            return [AllowAny()]
        return [IsAuthenticated(), IsProductOwner()]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return ProductUpdateSerializer
        return ProductDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.increment_view()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class ProductPublishView(APIView):
    """
    E'lonni moderatsiyadan aktivga o'tkazish.
    """
    permission_classes = [IsAuthenticated, IsProductOwner]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(request, product)

        if product.status not in ['moderatsiyada', 'arxivlangan']:
            return Response(
                {'error': f"Faqat moderatsiyada yoki arxivdagi e'lonni nashr etish mumkin. Hozirgi status: {product.status}"},
                status=status.HTTP_400_BAD_REQUEST
            )

        product.publish()
        return Response({'message': "E'lon muvaffaqiyatli nashr etildi.", 'status': product.status})


class ProductArchiveView(APIView):
    """
    E'lonni arxivlash.
    """
    permission_classes = [IsAuthenticated, IsProductOwner]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(request, product)

        if product.status == 'arxivlangan':
            return Response({'error': "E'lon allaqachon arxivlangan."}, status=status.HTTP_400_BAD_REQUEST)

        product.archive()
        return Response({'message': "E'lon arxivlandi.", 'status': product.status})


class ProductSoldView(APIView):
    """
    E'lonni sotilgan deb belgilash.
    """
    permission_classes = [IsAuthenticated, IsProductOwner]

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        self.check_object_permissions(request, product)

        if product.status == 'sotilgan':
            return Response({'error': "E'lon allaqachon sotilgan deb belgilangan."}, status=status.HTTP_400_BAD_REQUEST)

        product.mark_as_sold()
        return Response({'message': "E'lon sotilgan deb belgilandi.", 'status': product.status})


class MyProductsView(generics.ListAPIView):
    """
    Joriy sotuvchining o'z mahsulotlari (barcha statuslar).
    """
    serializer_class = ProductListSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(
            seller=self.request.user
        ).select_related('category').prefetch_related('images')
