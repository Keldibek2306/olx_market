import django_filters
from .models import Product


class ProductFilter(django_filters.FilterSet):
    
    category = django_filters.CharFilter(method='filter_by_category')
    min_price = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    max_price = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    region = django_filters.CharFilter(field_name='region', lookup_expr='icontains')
    condition = django_filters.CharFilter(field_name='condition', lookup_expr='exact')

    class Meta:
        model = Product
        fields = ['category', 'region', 'min_price', 'max_price', 'condition']

    def filter_by_category(self, queryset, name, value):
       
        if value.isdigit():
            return queryset.filter(category_id=int(value))
        return queryset.filter(category__slug=value)
