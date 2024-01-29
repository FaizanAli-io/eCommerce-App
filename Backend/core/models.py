from django.db import models

from django.contrib.auth.models import (
    PermissionsMixin,
    AbstractBaseUser,
    BaseUserManager,
)


class ConsumerManager(BaseUserManager):

    def create_user(self, email, password=None, **kwargs):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **kwargs)
        user.set_password(password)
        if kwargs['is_superuser']:
            user.is_staff = True

        user.save(using=self._db)
        return user


class Consumer(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    email = models.EmailField(max_length=255, unique=True)

    objects = ConsumerManager()

    USERNAME_FIELD = 'email'


class Vendor(models.Model):
    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)

    def __str__(self) -> str:
        return f'{self.name} - {self.desc}'


class Product(models.Model):
    seller = models.ForeignKey(Vendor, on_delete=models.CASCADE,
                               related_name="products")

    name = models.CharField(max_length=255)
    desc = models.TextField(blank=True)
    stock = models.IntegerField()
    price = models.FloatField()

    def __str__(self) -> str:
        return f'{self.name} - {self.seller.name}'
