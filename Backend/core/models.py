from django.db import models

from django.contrib.auth.models import (
    PermissionsMixin,
    AbstractBaseUser,
    BaseUserManager,
)


class ConsumerManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):
        user = self.model(self.normalize_email(email), **kwargs)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **kwargs):
        user = self.create_user(email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class Consumer(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

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
