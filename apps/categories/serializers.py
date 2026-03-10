from rest_framework import serializers
from .models import Category


class CategoryChildSerializer(serializers.ModelSerializer):
    """
    Ichki (child) kategoriyalar uchun serializer.
    """
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'icon', 'order_num']


class CategorySerializer(serializers.ModelSerializer):
    """
    Kategoriya uchun asosiy serializer (children bilan).
    """
    children = CategoryChildSerializer(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'icon', 'description', 'is_active', 'order_num', 'children', 'created_at']
        read_only_fields = ['id', 'created_at']


class CategoryDetailSerializer(serializers.ModelSerializer):
    """
    Kategoriya detail ko'rinish uchun serializer.
    """
    children = CategoryChildSerializer(many=True, read_only=True)
    parent = CategoryChildSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'parent', 'icon', 'description', 'is_active', 'order_num', 'children']
