from rest_framework.serializers import ModelSerializer

from product.serializers import ProductSerializer, ProductStockSerializer
from core.models import Transaction, ProductSold, Cart
from user.serializers import UserSerializer


class ProductSoldSerializer(ModelSerializer):

    product = ProductSerializer(read_only=True)

    class Meta:
        model = ProductSold
        fields = "__all__"


class CartSerializer(ModelSerializer):

    buyer = UserSerializer(read_only=True)
    product = ProductStockSerializer(read_only=True)

    class Meta:
        model = Cart
        fields = "__all__"


class TransactionSerializer(ModelSerializer):

    buyer = UserSerializer(read_only=True)
    product = ProductSoldSerializer(read_only=True)

    class Meta:
        model = Transaction
        fields = "__all__"
