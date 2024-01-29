from rest_framework.viewsets import ModelViewSet

from rest_framework.pagination import PageNumberPagination

from core.models import Consumer

from .serializers import ConsumerSerializer


class ConsumerViewSet(ModelViewSet):
    queryset = Consumer.objects.all()
    serializer_class = ConsumerSerializer
    pagination_class = PageNumberPagination
