from django.shortcuts import get_object_or_404
from rest_framework import generics
from addresses.permissions import IsFacilityOwner
from .serializers import AddressSerializer
from facilities.models import Facility
from rest_framework.authentication import TokenAuthentication
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Address'])
@extend_schema(description='User must be the owner or admin', methods=["PATCH", "PUT"])

class AddressView(generics.RetrieveUpdateAPIView):
    serializer_class = AddressSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsFacilityOwner]
    queryset = Facility.objects.all()

    lookup_url_kwarg = 'facility_id'

    def get_object(self):
        facility_instance = get_object_or_404(Facility, pk=self.kwargs["facility_id"])
        self.check_object_permissions(self.request, facility_instance)
        return facility_instance.address


