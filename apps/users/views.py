from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.exceptions import TokenError
from django.utils import timezone
from drf_spectacular.utils import extend_schema

from .models import User
from .serializers import (
    TelegramLoginSerializer, UserSerializer,
    UserUpdateSerializer, get_tokens_for_user
)


class TelegramLoginView(APIView):
    """
    Telegram orqali login yoki ro'yxatdan o'tish.
    Agar foydalanuvchi mavjud bo'lsa, tokenlar qaytariladi.
    Agar mavjud bo'lmasa, yangi foydalanuvchi yaratiladi.
    """
    permission_classes = [AllowAny]

    @extend_schema(
        request=TelegramLoginSerializer,
        responses={200: {'type': 'object', 'properties': {
            'access': {'type': 'string'},
            'refresh': {'type': 'string'},
            'user': {'type': 'object'},
            'created': {'type': 'boolean'},
        }}}
    )
    def post(self, request):
        serializer = TelegramLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        user, created = User.objects.get_or_create(
            telegram_id=data['telegram_id'],
            defaults={
                'username': data['username'],
                'first_name': data['first_name'],
                'last_name': data.get('last_name', ''),
                'role': 'customer',
            }
        )

        if not created:
            # Mavjud foydalanuvchi ma'lumotlarini yangilash
            user.username = data['username']
            user.first_name = data['first_name']
            user.last_name = data.get('last_name', user.last_name)
            user.last_login = timezone.now()
            user.save(update_fields=['username', 'first_name', 'last_name', 'last_login'])

        tokens = get_tokens_for_user(user)

        return Response({
            **tokens,
            'user': UserSerializer(user).data,
            'created': created,
        }, status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    Tokenni blacklistga qo'shish orqali chiqish.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request={'type': 'object', 'properties': {'refresh': {'type': 'string'}}},
        responses={200: {'type': 'object', 'properties': {'message': {'type': 'string'}}}}
    )
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if not refresh_token:
                return Response(
                    {'error': 'refresh token talab qilinadi.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': 'Muvaffaqiyatli chiqildi.'}, status=status.HTTP_200_OK)
        except TokenError:
            return Response(
                {'error': 'Noto\'g\'ri yoki muddati o\'tgan token.'},
                status=status.HTTP_400_BAD_REQUEST
            )


class UserProfileView(generics.RetrieveUpdateAPIView):
    """
    O'z profilini ko'rish va tahrirlash.
    """
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return UserUpdateSerializer
        return UserSerializer

    def get_object(self):
        return self.request.user


class UpgradeToSellerView(APIView):
    """
    Xaridorni sotuvchiga o'tkazish.
    SellerProfile yaratish uchun sellers app'idagi endpoint ishlatiladi.
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=None,
        responses={200: UserSerializer}
    )
    def post(self, request):
        user = request.user

        if user.is_seller:
            return Response(
                {'error': 'Siz allaqachon sotuvchisiz.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        user.role = 'seller'
        user.save(update_fields=['role'])

        return Response({
            'message': 'Siz muvaffaqiyatli sotuvchi bo\'ldingiz.',
            'user': UserSerializer(user).data,
        }, status=status.HTTP_200_OK)
