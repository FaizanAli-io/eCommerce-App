from rest_framework.serializers import ModelSerializer


from core.models import Transaction, ProductSold, Cart
from user.serializers import UserSerializer


class CartSerializer(ModelSerializer):

    consumer = UserSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"

    def update(self, instance, validated_data):
        validated_data.pop('product', None)
        return super().update(instance, validated_data)


class ProductSoldSerializer(ModelSerializer):

    class Meta:
        model = ProductSold
        fields = "__all__"


class TransactionSerializer(ModelSerializer):

    products = ProductSoldSerializer(many=True, read_only=True)
    consumer = UserSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = "__all__"