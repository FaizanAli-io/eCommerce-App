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
    UserSerializer,
    AuthTokenSerializer,
)


class UserListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()
    pagination_class = pagination.PageNumberPagination


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_object(self):
        return self.request.user


class CreateTokenView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
