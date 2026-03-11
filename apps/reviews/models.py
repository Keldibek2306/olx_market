from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator


class Review(models.Model):
    
    order = models.OneToOneField(
        'orders.Order',
        on_delete=models.CASCADE,
        related_name='review',
        verbose_name="Buyurtma"
    )
    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='given_reviews',
        verbose_name="Fikr qoldiruvchi"
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='received_reviews',
        verbose_name="Sotuvchi"
    )
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Reyting"
    )
    comment = models.TextField(verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Fikr"
        verbose_name_plural = "Fikrlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.reviewer.username} → {self.seller.username}: {self.rating}★"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self._update_seller_rating()

    def _update_seller_rating(self):
        """Sotuvchining umumiy reytingini qayta hisoblash."""
        if hasattr(self.seller, 'seller_profile'):
            self.seller.seller_profile.update_rating()
