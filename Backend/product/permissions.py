from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)

from django.contrib.auth import get_user_model

cat = get_user_model().UserCategory


class ProductAPIPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
            (request.method in SAFE_METHODS or
             request.user.category in (cat.VENDOR, cat.ADMIN))

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and \
            (request.method in SAFE_METHODS or
             request.user == obj.user)
