from rest_framework.permissions import BasePermission


class IsSeller(BasePermission):
    """
    Faqat sotuvchilarga ruxsat berish.
    """
    message = "Bu amal faqat sotuvchilar uchun."

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_seller


class IsSellerOwner(BasePermission):
    """
    Faqat o'z do'konini tahrirlashga ruxsat.
    """
    message = "Bu do'kon sizga tegishli emas."

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
