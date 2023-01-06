from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from facilities.models import Facility
from .permissions import IsOwner, IsTheOwnerOrAdmin
from .serializers import FacilitySerializer, DetailedFacilitySerializer
from django_filters import rest_framework as filters


class FacilityFilter(filters.FilterSet):
    city = filters.CharFilter(field_name="address__city", lookup_expr="icontains")

    class Meta:
        model = Facility
        fields = "__all__"


class FacilityView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsTheOwnerOrAdmin]
    
    serializer_class = FacilitySerializer
    queryset = Facility.objects.all()

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FacilityFilter


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class FacilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsTheOwnerOrAdmin]
    
    serializer_class = DetailedFacilitySerializer
    queryset = Facility.objects.all()
    lookup_url_kwarg = "sport_facility_id"


