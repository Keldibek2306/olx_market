from rest_framework import serializers
from .models import Review
from apps.users.serializers import UserSerializer


class ReviewSerializer(serializers.ModelSerializer):
   
    reviewer = UserSerializer(read_only=True)
    seller_name = serializers.CharField(source='seller.get_full_name', read_only=True)
    product_title = serializers.CharField(source='order.product.title', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'order', 'reviewer', 'seller_name', 'product_title',
            'rating', 'comment', 'created_at'
        ]
        read_only_fields = ['id', 'created_at']


class ReviewCreateSerializer(serializers.ModelSerializer):
    """
    Yangi fikr qoldirish uchun serializer.
    """
    order_id = serializers.IntegerField()

    class Meta:
        model = Review
        fields = ['order_id', 'rating', 'comment']

    def validate_order_id(self, value):
        from apps.orders.models import Order
        user = self.context['request'].user

        try:
            order = Order.objects.get(pk=value, buyer=user)
        except Order.DoesNotExist:
            raise serializers.ValidationError("Buyurtma topilmadi yoki siz bu buyurtmaning xaridori emassiz.")

        if order.status != 'sotib_olingan':
            raise serializers.ValidationError("Faqat 'sotib olingan' buyurtma uchun fikr qoldirish mumkin.")

        if hasattr(order, 'review'):
            raise serializers.ValidationError("Bu buyurtma uchun allaqachon fikr qoldirgan.")

        return value

    def create(self, validated_data):
        from apps.orders.models import Order
        user = self.context['request'].user
        order = Order.objects.get(pk=validated_data.pop('order_id'))

        return Review.objects.create(
            order=order,
            reviewer=user,
            seller=order.seller,
            **validated_data
        )
