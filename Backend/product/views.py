from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication

from core.models import ProductStock
from .serializers import ProductStockSerializer
from .permissions import ProductAPIPermission

"""

    Views:-
        1. Product List View
        2. Get Specific Product View
        3. Update Product View (auth)
        4. Delete Product View (auth)
        5. Create Product View (auth)

"""


class ProductViewSet(ModelViewSet):
    pagination_class = PageNumberPagination
    serializer_class = ProductStockSerializer
    queryset = ProductStock.objects.order_by()
    permission_classes = [ProductAPIPermission]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        vendor = self.request.user
        serializer.save(vendor=vendor)
