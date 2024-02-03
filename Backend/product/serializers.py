from rest_framework.serializers import (
    ModelSerializer,
    StringRelatedField,
)

from core.models import Product


class ProductSerializer(ModelSerializer):

    user = StringRelatedField()

    class Meta:
        model = Product
        fields = "__all__"
        read_only_fields = ['user']
