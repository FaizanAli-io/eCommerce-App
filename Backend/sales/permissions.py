from rest_framework.permissions import BasePermission

from django.contrib.auth import get_user_model

cat = get_user_model().UserCategory


class CartAPIPermission(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and \
            request.user.category in (cat.CONSUMER, cat.ADMIN)

    def has_object_permission(self, request, view, obj):
        return request.user.is_authenticated and \
            request.user == obj.consumer
