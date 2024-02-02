from rest_framework import (
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


class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer
    queryset = get_user_model().objects.all()


class TokenCreateView(ObtainAuthToken):
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class TokenDeleteView(generics.DestroyAPIView):
    serializer_class = AuthTokenSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_object(self):
        return self.request.user.auth_token


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_object(self):
        return self.request.user
