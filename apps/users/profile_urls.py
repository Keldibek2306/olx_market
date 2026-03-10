from django.urls import path
from .views import UserProfileView, UpgradeToSellerView

urlpatterns = [
    path('me/', UserProfileView.as_view(), name='user-profile'),
    path('me/upgrade-to-seller/', UpgradeToSellerView.as_view(), name='upgrade-to-seller'),
]
