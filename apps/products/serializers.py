from rest_framework import serializers
from .models import Product, ProductImage
from apps.users.serializers import UserSerializer


class ProductImageSerializer(serializers.ModelSerializer):
    """
    Mahsulot rasmi uchun serializer.
    """
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'order', 'is_main']


class ProductListSerializer(serializers.ModelSerializer):
    """
    Mahsulotlar ro'yxati uchun qisqa serializer.
    """
    main_image = serializers.SerializerMethodField()
    category_name = serializers.CharField(source='category.name', read_only=True)
    seller_name = serializers.CharField(source='seller.get_full_name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'price', 'price_type', 'condition',
            'region', 'district', 'status', 'view_count', 'favorite_count',
            'main_image', 'category_name', 'seller_name', 'created_at'
        ]

    def get_main_image(self, obj):
        main = obj.images.filter(is_main=True).first()
        if not main:
            main = obj.images.first()
        if main:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri(main.image.url)
            return main.image.url
        return None


class ProductDetailSerializer(serializers.ModelSerializer):
    """
    Mahsulot detail ko'rinishi uchun serializer.
    """
    images = ProductImageSerializer(many=True, read_only=True)
    seller = UserSerializer(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'seller', 'category', 'category_name', 'title', 'description',
            'condition', 'price', 'price_type', 'region', 'district',
            'view_count', 'favorite_count', 'status',
            'images', 'created_at', 'updated_at', 'published_at', 'expires_at'
        ]


class ProductCreateSerializer(serializers.ModelSerializer):
    """
    Mahsulot yaratish uchun serializer.
    """
    images = serializers.ListField(
        child=serializers.ImageField(), write_only=True, required=False
    )

    class Meta:
        model = Product
        fields = [
            'category', 'title', 'description', 'condition', 'price',
            'price_type', 'region', 'district', 'images'
        ]

    def create(self, validated_data):
        images_data = validated_data.pop('images', [])
        validated_data['seller'] = self.context['request'].user
        product = Product.objects.create(**validated_data)

        for index, image in enumerate(images_data):
            ProductImage.objects.create(
                product=product,
                image=image,
                order=index,
                is_main=(index == 0)
            )
        return product


class ProductUpdateSerializer(serializers.ModelSerializer):
    """
    Mahsulot yangilash uchun serializer.
    """
    class Meta:
        model = Product
        fields = [
            'category', 'title', 'description', 'condition', 'price',
            'price_type', 'region', 'district'
        ]

    def update(self, instance, validated_data):
        """Aktiv e'lon tahrirlanganida moderatsiyaga o'tkazish."""
        if instance.status == 'aktiv':
            validated_data['status'] = 'moderatsiyada'
        return super().update(instance, validated_data)
