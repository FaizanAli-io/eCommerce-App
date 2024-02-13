from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import RetrieveAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication

from core.models import Cart, Transaction

from .serializers import CartSerializer, TransactionSerializer


class CartViewSet(ModelViewSet):
    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    pagination_class = PageNumberPagination

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def perform_create(self, serializer):
        consumer = self.request.user
        serializer.save(consumer=consumer)


class RetrieveTransactionsAPIView(RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]
