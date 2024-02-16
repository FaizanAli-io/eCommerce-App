from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication

from core.models import Cart, Transaction

from .permissions import CartAPIPermission
from .serializers import CartSerializer, TransactionSerializer


class CartViewSet(ModelViewSet):
    serializer_class = CartSerializer
    pagination_class = PageNumberPagination

    permission_classes = [CartAPIPermission]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return Cart.objects.filter(consumer=self.request.user)

    def perform_create(self, serializer):
        consumer = self.request.user
        serializer.save(consumer=consumer)


class RetrieveTransactionsAPIView(RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
