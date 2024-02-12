from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
)

from core.models import Product, ProductStock


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        exclude = ['id']


class ProductStockSerializer(ModelSerializer):

    product = ProductSerializer()

    vendor = StringRelatedField()

    class Meta:
        model = ProductStock
        exclude = ['id']

    def create(self, validated_data):
        product_data = validated_data.pop('product')
        product = Product.objects.create(**product_data)
        product_stock = ProductStock.objects.create(
            product=product, **validated_data)
        return product_stock

    def update(self, instance, validated_data):
        product_data = validated_data.pop('product', {})
        product = instance.product

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        for attr, value in product_data.items():
            setattr(product, attr, value)
        product.save()

        return instance
