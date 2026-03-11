from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Product(models.Model):
    """
    Mahsulot (e'lon) modeli.
    """
    CONDITION_CHOICES = (
        ('yangi', 'Yangi'),
        ('ideal', 'Ideal'),
        ('yaxshi', 'Yaxshi'),
        ('qoniqarli', 'Qoniqarli'),
    )

    PRICE_TYPE_CHOICES = (
        ('qatiy', "Qat'iy"),
        ('kelishiladi', 'Kelishiladi'),
        ('bepul', 'Bepul'),
        ('ayirboshlash', 'Ayirboshlash'),
    )

    STATUS_CHOICES = (
        ('moderatsiyada', 'Moderatsiyada'),
        ('aktiv', 'Aktiv'),
        ('rad_etilgan', 'Rad etilgan'),
        ('sotilgan', 'Sotilgan'),
        ('arxivlangan', 'Arxivlangan'),
    )

    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Sotuvchi"
    )
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        null=True,
        related_name='products',
        verbose_name="Kategoriya"
    )
    title = models.CharField(max_length=200, verbose_name="Sarlavha")
    description = models.TextField(verbose_name="Tavsif")
    condition = models.CharField(max_length=20, choices=CONDITION_CHOICES, verbose_name="Holati")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Narx")
    price_type = models.CharField(max_length=20, choices=PRICE_TYPE_CHOICES, default='qatiy', verbose_name="Narx turi")
    region = models.CharField(max_length=100, verbose_name="Viloyat")
    district = models.CharField(max_length=100, verbose_name="Tuman")
    view_count = models.PositiveIntegerField(default=0, verbose_name="Ko'rishlar soni")
    favorite_count = models.PositiveIntegerField(default=0, verbose_name="Sevimlilar soni")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='moderatsiyada', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True, verbose_name="Nashr vaqti")
    expires_at = models.DateTimeField(null=True, blank=True, verbose_name="Amal qilish muddati")

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} ({self.get_status_display()})"

    def publish(self):
        """E'lonni chop etish (moderatsiyadan aktivga)."""
        self.status = 'aktiv'
        self.published_at = timezone.now()
        self.expires_at = timezone.now() + timedelta(days=30)
        self.save(update_fields=['status', 'published_at', 'expires_at'])

    def archive(self):
        
        self.status = 'arxivlangan'
        self.save(update_fields=['status'])

    def mark_as_sold(self):
        self.status = 'sotilgan'
        self.save(update_fields=['status'])
        
        if hasattr(self.seller, 'seller_profile'):
            self.seller.seller_profile.total_sales += 1
            self.seller.seller_profile.save(update_fields=['total_sales'])

    def increment_view(self):
        Product.objects.filter(pk=self.pk).update(view_count=models.F('view_count') + 1)


class ProductImage(models.Model):
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Mahsulot"
    )
    image = models.ImageField(upload_to='products/', verbose_name="Rasm")
    order = models.PositiveIntegerField(default=0, verbose_name="Tartib")
    is_main = models.BooleanField(default=False, verbose_name="Asosiy rasm")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mahsulot rasmi"
        verbose_name_plural = "Mahsulot rasmlari"
        ordering = ['order']

    def save(self, *args, **kwargs):
        if self.is_main:
            ProductImage.objects.filter(
                product=self.product, is_main=True
            ).exclude(pk=self.pk).update(is_main=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.title} - Rasm {self.order}"
