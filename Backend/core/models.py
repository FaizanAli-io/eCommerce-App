from django.db import models

from django.contrib.auth.models import (
    PermissionsMixin,
    AbstractBaseUser,
    BaseUserManager,
)

from django.conf import settings

from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, clean_user=True, **kwargs):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)

        if kwargs.get('category') == User.UserCategory.ADMIN:
            user.is_superuser = True
            user.is_staff = True

        user.save()
        if clean_user:
            user.full_clean()

        return user

    def create_superuser(self, email, password):
        return self.create_user(email, password, clean_user=False,
                                category=User.UserCategory.ADMIN)


class User(AbstractBaseUser, PermissionsMixin):

    class UserCategory(models.TextChoices):
        CONSUMER = 0, _('Consumer')
        VENDOR = 1, _('Vendor')
        ADMIN = 2, _('Admin')

    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    category = models.CharField(
        max_length=10,
        choices=UserCategory.choices,
        default=UserCategory.CONSUMER,
    )

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    objects = UserManager()

    def __str__(self) -> str:
        return self.name


class Transaction(models.Model):
    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    listed_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)

    def __str__(self) -> str:
        return self.name


class ProductStock(models.Model):
    vendor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.IntegerField()
    price = models.FloatField()

    def __str__(self) -> str:
        return f"{self.product} - {self.vendor}"


class ProductSold(models.Model):
    transaction = models.ForeignKey(Transaction, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.IntegerField()
    price = models.FloatField()

    def __str__(self) -> str:
        return f"{self.product} - {self.transaction.id}"


class Cart(models.Model):
    buyer = models.ForeignKey(settings.AUTH_USER_MODEL,
                              on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    stock = models.IntegerField()
    price = models.FloatField()

    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.buyer.name} - {self.product.name}"
