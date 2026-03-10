from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsSellerOrReadOnly(BasePermission):
    """
    O'qish - hammaga, yozish - faqat sellerlarga.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user.is_authenticated and request.user.is_seller


class IsProductOwner(BasePermission):
    """
    Faqat mahsulot egasiga tahrirlash/o'chirish ruxsati.
    """
    message = "Bu mahsulot sizga tegishli emas."

    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user
