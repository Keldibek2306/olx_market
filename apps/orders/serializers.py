from rest_framework import serializers
from .models import Order
from apps.products.serializers import ProductListSerializer
from apps.users.serializers import UserSerializer


class OrderListSerializer(serializers.ModelSerializer):
    """
    Buyurtmalar ro'yxati uchun serializer.
    """
    product = ProductListSerializer(read_only=True)
    buyer_name = serializers.CharField(source='buyer.get_full_name', read_only=True)
    seller_name = serializers.CharField(source='seller.get_full_name', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'product', 'buyer_name', 'seller_name', 'final_price',
            'status', 'meeting_location', 'meeting_time', 'notes',
            'created_at', 'updated_at'
        ]


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Buyurtma detail ko'rinishi uchun serializer.
    """
    product = ProductListSerializer(read_only=True)
    buyer = UserSerializer(read_only=True)
    seller = UserSerializer(read_only=True)
    has_review = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id', 'product', 'buyer', 'seller', 'final_price',
            'status', 'meeting_location', 'meeting_time', 'notes',
            'has_review', 'created_at', 'updated_at'
        ]

    def get_has_review(self, obj):
        return hasattr(obj, 'review')


class OrderCreateSerializer(serializers.ModelSerializer):
    """
    Yangi buyurtma yaratish uchun serializer.
    """
    product_id = serializers.IntegerField()

    class Meta:
        model = Order
        fields = ['product_id', 'notes']

    def validate_product_id(self, value):
        from apps.products.models import Product
        try:
            product = Product.objects.get(pk=value, status='aktiv')
        except Product.DoesNotExist:
            raise serializers.ValidationError("Bunday aktiv mahsulot topilmadi.")
        return value

    def validate(self, attrs):
        from apps.products.models import Product
        user = self.context['request'].user
        product = Product.objects.get(pk=attrs['product_id'])

        if product.seller == user:
            raise serializers.ValidationError("O'z mahsulotingizga buyurtma bera olmaysiz.")

        # Allaqachon aktiv buyurtma bormi?
        if Order.objects.filter(
            product=product, buyer=user,
            status__in=['kutilyapti', 'kelishilgan']
        ).exists():
            raise serializers.ValidationError("Bu mahsulotga allaqachon aktiv buyurtmangiz bor.")

        return attrs

    def create(self, validated_data):
        from apps.products.models import Product
        user = self.context['request'].user
        product = Product.objects.get(pk=validated_data.pop('product_id'))

        return Order.objects.create(
            product=product,
            buyer=user,
            seller=product.seller,
            final_price=product.price,
            **validated_data
        )


class OrderUpdateSerializer(serializers.ModelSerializer):
    """
    Buyurtma statusini yangilash uchun serializer.
    Sotuvchi: kutilyapti → kelishilgan yoki bekor_qilingan
    Xaridor: kelishilgan → sotib_olingan yoki bekor_qilingan
    """
    class Meta:
        model = Order
        fields = ['status', 'final_price', 'meeting_location', 'meeting_time']

    def validate_status(self, value):
        user = self.context['request'].user
        order = self.instance

        if user == order.seller:
            allowed = {'kutilyapti': ['kelishilgan', 'bekor_qilingan']}
        elif user == order.buyer:
            allowed = {'kelishilgan': ['sotib_olingan', 'bekor_qilingan']}
        else:
            raise serializers.ValidationError("Sizda bu buyurtmani o'zgartirish huquqi yo'q.")

        current = order.status
        if current not in allowed or value not in allowed.get(current, []):
            raise serializers.ValidationError(
                f"'{current}' statusidan '{value}' ga o'tish mumkin emas."
            )
        return value

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)

        # Sotib olinganida mahsulotni yopish
        if instance.status == 'sotib_olingan':
            instance.product.mark_as_sold()

        return instance
