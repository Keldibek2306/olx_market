from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken
from django.utils import timezone
from .models import User


class TelegramLoginSerializer(serializers.Serializer):
   
    telegram_id = serializers.IntegerField()
    username = serializers.CharField(max_length=150)
    first_name = serializers.CharField(max_length=150)
    last_name = serializers.CharField(max_length=150, required=False, default='')
    photo_url = serializers.URLField(required=False, allow_blank=True)

    def validate_telegram_id(self, value):
        if value <= 0:
            raise serializers.ValidationError("Noto'g'ri Telegram ID.")
        return value


class UserSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = User
        fields = [
            'id', 'telegram_id', 'username', 'first_name', 'last_name',
            'phone_number', 'role', 'avatar', 'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'telegram_id', 'username', 'role', 'is_active', 'date_joined']


class UserUpdateSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'avatar']


class TokenSerializer(serializers.Serializer):
    
    access = serializers.CharField()
    refresh = serializers.CharField()
    user = UserSerializer()


def get_tokens_for_user(user):
  
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh),
    }
