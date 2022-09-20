from rest_framework import permissions
from rest_framework.views import Request, View
from users.models import User

from .models import PaymentInformation



class IsOwner(permissions.BasePermission):
    
    def has_object_permission(self, request: Request, view: View, obj):
        if request.method == 'POST':
                            
            return (request.user.is_authenticated and request.user.id==obj.user_id)
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
        if request.method == 'DELETE' or 'GET':
            return request.user.is_superuser or (request.user.id == obj.user_id)
        
        return request.user == obj.user
    
class IsAuthenticated(permissions.BasePermission):
    def has_permission(self, request: Request, view: View) -> bool:
        
        return request.user.is_authenticated
