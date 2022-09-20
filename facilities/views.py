from django.shortcuts import render
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication

from facilities.models import Facility

from .permissions import IsOwner, IsTheOwner, IsTheOwnerOrAdmin
from .serializers import FacilitySerializer, DetailedFacilitySerializer


class FacilityView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwner]
    serializer_class = FacilitySerializer
    queryset = Facility.objects.all()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class FacilityDetailView(generics.RetrieveUpdateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsTheOwner]
    serializer_class = DetailedFacilitySerializer
    queryset = Facility.objects.all()
    lookup_url_kwarg = "sport_facility_id"

class FacilityDeleteView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsTheOwnerOrAdmin]
    serializer_class = FacilitySerializer
    queryset = Facility.objects.all()
    lookup_url_kwarg = "sport_facility_id"
