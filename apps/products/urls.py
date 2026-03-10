from django.urls import path
from .views import (
    ProductListCreateView, ProductDetailView,
    ProductPublishView, ProductArchiveView, ProductSoldView, MyProductsView
)

urlpatterns = [
    path('', ProductListCreateView.as_view(), name='product-list'),
    path('my/', MyProductsView.as_view(), name='my-products'),
    path('<int:pk>/', ProductDetailView.as_view(), name='product-detail'),
    path('<int:pk>/publish/', ProductPublishView.as_view(), name='product-publish'),
    path('<int:pk>/archive/', ProductArchiveView.as_view(), name='product-archive'),
    path('<int:pk>/sold/', ProductSoldView.as_view(), name='product-sold'),
]
