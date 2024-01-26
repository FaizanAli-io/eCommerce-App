from django.db import models


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
