from django.db import models
from users.models import CustomUser
from rest_framework.permissions import BasePermission


class IsModerator(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if not request.user.is_staff:
            return False

        if request.method == "POST":
            return False

        return True

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff