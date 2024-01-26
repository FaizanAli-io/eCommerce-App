from rest_framework.serializers import ModelSerializer

from core.models import (
    Vendor,
    Product,
)


class ProductSerializer(ModelSerializer):

    class Meta:
        model = Product
        fields = "__all__"


class VendorSerializer(ModelSerializer):

    products = ProductSerializer(many=True, read_only=True)

    class Meta:
        model = Vendor
        fields = "__all__"
