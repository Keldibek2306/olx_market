from django.db import models
from django.conf import settings


class Order(models.Model):
    """
    Buyurtma modeli.
    """
    STATUS_CHOICES = (
        ('kutilyapti', 'Kutilyapti'),
        ('kelishilgan', 'Kelishilgan'),
        ('sotib_olingan', 'Sotib olingan'),
        ('bekor_qilingan', 'Bekor qilingan'),
    )

    product = models.ForeignKey(
        'products.Product',
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name="Mahsulot"
    )
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='purchases',
        verbose_name="Xaridor"
    )
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='sales',
        verbose_name="Sotuvchi"
    )
    final_price = models.DecimalField(
        max_digits=12, decimal_places=2,
        verbose_name="Kelishilgan narx"
    )
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES,
        default='kutilyapti', verbose_name="Status"
    )
    meeting_location = models.CharField(max_length=300, blank=True, verbose_name="Uchrashuv joyi")
    meeting_time = models.DateTimeField(null=True, blank=True, verbose_name="Uchrashuv vaqti")
    notes = models.TextField(blank=True, verbose_name="Izoh")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Buyurtma"
        verbose_name_plural = "Buyurtmalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"Buyurtma #{self.pk} - {self.product.title}"
