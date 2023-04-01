from rest_framework import permissions
from courts.models import Court


class IsFacilityOwner(permissions.BasePermission):
    def has_permission(self, request, view):
        court_id = view.kwargs["court_id"]
        court = Court.objects.get(id=court_id)

        return request.user == court.sport_facility.user


class IsOwnerOrFacilityOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        
        court = obj.court
        facility_owner = court.sport_facility.user

        return (request.user == obj.user) or (request.user == facility_owner) or request.user.is_superuser