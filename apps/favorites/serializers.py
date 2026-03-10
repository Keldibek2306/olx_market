from rest_framework import serializers
from .models import Favorite
from apps.products.serializers import ProductListSerializer


class FavoriteSerializer(serializers.ModelSerializer):
    """
    Sevimlilar ro'yxati uchun serializer.
    """
    product = ProductListSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'product', 'created_at']
        read_only_fields = ['id', 'created_at']


class FavoriteCreateSerializer(serializers.ModelSerializer):
    """
    Sevimlilarga qo'shish uchun serializer.
    """
    product_id = serializers.IntegerField()

    class Meta:
        model = Favorite
        fields = ['product_id']

    def validate_product_id(self, value):
        from apps.products.models import Product
        try:
            Product.objects.get(pk=value, status='aktiv')
        except Product.DoesNotExist:
            raise serializers.ValidationError("Bunday aktiv mahsulot topilmadi.")
        return value

    def validate(self, attrs):
        user = self.context['request'].user
        if Favorite.objects.filter(user=user, product_id=attrs['product_id']).exists():
            raise serializers.ValidationError("Bu mahsulot allaqachon sevimlilarda.")
        return attrs

    def create(self, validated_data):
        from apps.products.models import Product
        user = self.context['request'].user
        product = Product.objects.get(pk=validated_data['product_id'])
        favorite = Favorite.objects.create(user=user, product=product)
        # favorite_count ni oshirish
        Product.objects.filter(pk=product.pk).update(
            favorite_count=product.favorite_count + 1
        )
        return favorite
