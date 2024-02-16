from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication

from core.models import ProductStock
from .permissions import ProductAPIPermission
from .serializers import ProductStockSerializer


class ProductViewSet(ModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = ProductStockSerializer
    queryset = ProductStock.objects.order_by()
    permission_classes = [ProductAPIPermission]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        vendor = self.request.user
        serializer.save(vendor=vendor)
