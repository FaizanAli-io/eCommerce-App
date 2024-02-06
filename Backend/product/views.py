from rest_framework.viewsets import ModelViewSet
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication

from core.models import Product
from .serializers import ProductSerializer
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
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination
    queryset = Product.objects.order_by('name')
    permission_classes = [ProductAPIPermission]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        user = self.request.user
        serializer.save(user=user)
