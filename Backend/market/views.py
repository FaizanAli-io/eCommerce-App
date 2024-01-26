from rest_framework.viewsets import ModelViewSet

from core.models import (
    Vendor,
    Product,
)

from .serializers import (
    VendorSerializer,
    ProductSerializer,
)


class VendorViewSet(ModelViewSet):
    queryset = Vendor.objects.all()
    serializer_class = VendorSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
