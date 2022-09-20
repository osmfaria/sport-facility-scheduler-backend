from rest_framework import permissions
        
class IsOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == "DELETE" or request.method == "GET":
            return request.user.is_superuser or request.user == obj
        
        return request.user == obj
        