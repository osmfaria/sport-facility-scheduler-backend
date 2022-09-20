from rest_framework import permissions
from courts.models import Court

import ipdb
        
class ReviewCustomPermission(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        if request.method == 'POST':
            return request.user.is_authenticated
        
        if request.method == 'PATCH':
            return  request.user == obj.user

        if request.method == 'DELETE':
            return request.user.is_superuser or request.user == obj.user
        
        return True
        