from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication

# from django.contrib.auth import get_user_model

from core.models import (
    Cart,
)

from .serializers import (
    CartSerializer,
)


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    queryset = Cart.objects.order_by()
    permission_classes = [IsAuthenticated]
    pagination_class = PageNumberPagination
    authentication_classes = [TokenAuthentication]
