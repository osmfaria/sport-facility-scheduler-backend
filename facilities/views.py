from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from facilities.models import Facility
from .permissions import IsTheOwnerOrAdmin
from .serializers import FacilitySerializer, DetailedFacilitySerializer
from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema



class FacilityFilter(filters.FilterSet):
    city = filters.CharFilter(field_name="address__city", lookup_expr="icontains")

    class Meta:
        model = Facility
        fields = "__all__"

@extend_schema(tags=['Sport_Facility'])
@extend_schema(description='Only allowed for User with is_owner=true', methods=["POST"])

class FacilityView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsTheOwnerOrAdmin]
    
    serializer_class = FacilitySerializer
    queryset = Facility.objects.all()

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FacilityFilter


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

@extend_schema(tags=['Sport_Facility'])
@extend_schema(description='User must be the owner or admin', methods=["PATCH", "DELETE"])
@extend_schema(exclude=True, methods=["PUT"])

class FacilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsTheOwnerOrAdmin]
    
    serializer_class = DetailedFacilitySerializer
    queryset = Facility.objects.all()
    lookup_url_kwarg = "sport_facility_id"


