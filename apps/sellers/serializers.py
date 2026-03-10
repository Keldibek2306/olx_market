from rest_framework import serializers
from .models import SellerProfile
from apps.users.serializers import UserSerializer


class SellerProfileSerializer(serializers.ModelSerializer):
    """
    Sotuvchi profili uchun serializer.
    """
    user = UserSerializer(read_only=True)

    class Meta:
        model = SellerProfile
        fields = [
            'id', 'user', 'shop_name', 'shop_description', 'shop_logo',
            'region', 'district', 'address', 'rating', 'total_sales',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'user', 'rating', 'total_sales', 'created_at', 'updated_at']


class SellerProfileCreateSerializer(serializers.ModelSerializer):
    """
    Sotuvchi profili yaratish uchun serializer.
    """
    class Meta:
        model = SellerProfile
        fields = ['shop_name', 'shop_description', 'shop_logo', 'region', 'district', 'address']

    def validate(self, attrs):
        user = self.context['request'].user
        if hasattr(user, 'seller_profile'):
            raise serializers.ValidationError("Siz allaqachon do'kon profiliga egasiz.")
        if not user.is_seller:
            raise serializers.ValidationError(
                "Faqat sotuvchilar do'kon profili yarata oladi. Avval sotuvchiga o'ting."
            )
        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class SellerProfileUpdateSerializer(serializers.ModelSerializer):
    """
    Sotuvchi profilini yangilash uchun serializer.
    """
    class Meta:
        model = SellerProfile
        fields = ['shop_name', 'shop_description', 'shop_logo', 'region', 'district', 'address']
