from rest_framework.viewsets import ModelViewSet

from rest_framework.pagination import PageNumberPagination

from core.models import Product

from .serializers import ProductSerializer


class ProductViewSet(ModelViewSet):
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    queryset = Product.objects.order_by('name')
