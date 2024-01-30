from rest_framework import (
    pagination,
    permissions,
    authentication,
)

from rest_framework.viewsets import generics
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken

from django.contrib.auth import get_user_model

from .serializers import (
    ConsumerSerializer,
    AuthTokenSerializer,
)


class ConsumerListView(generics.ListCreateAPIView):
    serializer_class = ConsumerSerializer
    queryset = get_user_model().objects.all()
    pagination_class = pagination.PageNumberPagination


class ConsumerDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ConsumerSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
