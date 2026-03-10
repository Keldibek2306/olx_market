from django.urls import path
from .views import (
    SellerProfileCreateView, SellerProfileDetailView,
    PublicSellerDetailView, SellerProductsView
)

urlpatterns = [
    path('', SellerProfileCreateView.as_view(), name='seller-create'),
    path('me/', SellerProfileDetailView.as_view(), name='seller-me'),
    path('<int:seller_id>/', PublicSellerDetailView.as_view(), name='seller-detail'),
    path('<int:seller_id>/products/', SellerProductsView.as_view(), name='seller-products'),
]
