from django.db import models
from django.conf import settings


class SellerProfile(models.Model):
    """
    Sotuvchi profili. User modeli bilan OneToOne bog'lanish.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='seller_profile',
        verbose_name="Foydalanuvchi"
    )
    shop_name = models.CharField(max_length=200, unique=True, verbose_name="Do'kon nomi")
    shop_description = models.TextField(blank=True, verbose_name="Do'kon tavsifi")
    shop_logo = models.ImageField(upload_to='shop_logos/', blank=True, null=True, verbose_name="Do'kon logosi")
    region = models.CharField(max_length=100, verbose_name="Viloyat")
    district = models.CharField(max_length=100, verbose_name="Tuman")
    address = models.CharField(max_length=300, blank=True, verbose_name="Manzil")
    rating = models.FloatField(default=0.0, verbose_name="Reyting")
    total_sales = models.PositiveIntegerField(default=0, verbose_name="Sotuvlar soni")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Sotuvchi profili"
        verbose_name_plural = "Sotuvchi profillari"

    def __str__(self):
        return f"{self.shop_name} ({self.user.username})"

    def update_rating(self):
        """
        Barcha fikrlar asosida reytingni qayta hisoblash.
        """
        from apps.reviews.models import Review
        reviews = Review.objects.filter(seller=self.user)
        if reviews.exists():
            total = sum(r.rating for r in reviews)
            self.rating = round(total / reviews.count(), 2)
        else:
            self.rating = 0.0
        self.save(update_fields=['rating'])
