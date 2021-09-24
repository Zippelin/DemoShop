from rest_framework.permissions import BasePermission
from .models import User
from utils.response import get_error_message, \
    C_NOT_PROVIDER, \
    C_NOT_CUSTOMER


class UserIsCustomer(BasePermission):
    message = get_error_message(C_NOT_CUSTOMER)

    def has_permission(self, request, view):
        return request.user.type == User.Type.CUSTOMER


class UserIsProvider(BasePermission):
    message = get_error_message(C_NOT_PROVIDER)

    def has_permission(self, request, view):
        return request.user.type == User.Type.PROVIDER


class UserIsCustomerOrAdmin(BasePermission):
    message = get_error_message(C_NOT_CUSTOMER)

    def has_permission(self, request, view):
        return request.user.type == User.Type.CUSTOMER or request.user.is_superuser


class UserIsProviderOrAdmin(BasePermission):
    message = get_error_message(C_NOT_PROVIDER)

    def has_permission(self, request, view):
        return request.user.type == User.Type.PROVIDER or request.user.is_superuser
