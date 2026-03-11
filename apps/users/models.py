from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
   
    ROLE_CHOICES = (
        ('customer', 'Xaridor'),
        ('seller', 'Sotuvchi'),
    )

    telegram_id = models.BigIntegerField(unique=True, null=True, blank=True)
    username = models.CharField(max_length=150, unique=True, verbose_name="Username")
    first_name = models.CharField(max_length=150, verbose_name="Ism")
    last_name = models.CharField(max_length=150, blank=True, verbose_name="Familiya")
    phone_number = models.CharField(max_length=20, blank=True, verbose_name="Telefon raqam")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='customer', verbose_name="Rol")
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Profil rasmi")
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(null=True, blank=True)

    password = models.CharField(max_length=128, blank=True, default='')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['telegram_id', 'first_name']

    class Meta:
        verbose_name = "Foydalanuvchi"
        verbose_name_plural = "Foydalanuvchilar"
        ordering = ['-date_joined']

    def __str__(self):
        return f"{self.get_full_name()} (@{self.username})"

    @property
    def is_seller(self):
        return self.role == 'seller'

    @property
    def is_customer(self):
        return self.role == 'customer'
