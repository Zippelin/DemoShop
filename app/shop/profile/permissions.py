from rest_framework.permissions import BasePermission
from .models import User


class UserIsCustomer(BasePermission):
    message = 'You must be customer for that'

    def has_permission(self, request, view):
        return request.user.type == User.Type.CUSTOMER


class UserIsProvider(BasePermission):
    message = 'You must be provider for that'

    def has_permission(self, request, view):
        return request.user.type == User.Type.PROVIDER


class UserIsCustomerOrAdmin(BasePermission):
    message = 'You must be customer for that'

    def has_permission(self, request, view):
        return request.user.type == User.Type.CUSTOMER or request.user.is_superuser


class UserIsProviderOrAdmin(BasePermission):
    message = 'You must be provider for that'

    def has_permission(self, request, view):
        return request.user.type == User.Type.PROVIDER or request.user.is_superuser
