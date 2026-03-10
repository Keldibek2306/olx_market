from django.db import models
from django.utils.text import slugify


class Category(models.Model):
    """
    Ierarxik kategoriya modeli (parent-child tuzilish).
    """
    name = models.CharField(max_length=200, verbose_name="Nomi")
    slug = models.SlugField(unique=True, verbose_name="Slug")
    parent = models.ForeignKey(
        'self',
        null=True, blank=True,
        on_delete=models.SET_NULL,
        related_name='children',
        verbose_name="Ota kategoriya"
    )
    icon = models.ImageField(upload_to='category_icons/', blank=True, null=True, verbose_name="Ikonka")
    description = models.TextField(blank=True, verbose_name="Tavsif")
    is_active = models.BooleanField(default=True, verbose_name="Faolmi")
    order_num = models.PositiveIntegerField(default=0, verbose_name="Tartib raqami")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"
        ordering = ['order_num', 'name']

    def __str__(self):
        if self.parent:
            return f"{self.parent.name} → {self.name}"
        return self.name

    def save(self, *args, **kwargs):
        """Slug avtomatik yaratiladi."""
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    @property
    def is_root(self):
        """Ota kategoriyami?"""
        return self.parent is None

    def get_all_children(self):
        """Barcha ichki kategoriyalarni qaytarish."""
        children = list(self.children.filter(is_active=True))
        for child in self.children.filter(is_active=True):
            children.extend(child.get_all_children())
        return children
