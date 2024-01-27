from rest_framework.viewsets import ModelViewSet

from rest_framework.pagination import PageNumberPagination

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
    pagination_class = PageNumberPagination


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
