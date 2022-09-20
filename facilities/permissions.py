from rest_framework import permissions
from rest_framework.views import Request, View

from facilities.models import Facility


class IsOwner(permissions.BasePermission):
    def has_permission(self, request: Request, view:View) -> bool:
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user.is_owner


class IsTheOwner(permissions.BasePermission):
   def has_object_permission(self, request: Request, view: View, facility: Facility) -> bool:
        return request.user.id == facility.user.id


class IsTheOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request: Request, view: View, facility: Facility) -> bool:
        if request.user.is_superuser:
            return True
        return request.user.id == facility.user.id
