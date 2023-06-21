from django_filters import rest_framework as filters
from drf_spectacular.utils import extend_schema
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework import status

from facilities.models import Facility

from .permissions import IsTheOwner, IsTheOwnerOrAdmin
from .serializers import DetailedFacilitySerializer, FacilitySerializer


class FacilityFilter(filters.FilterSet):
    city = filters.CharFilter(field_name="address__city", lookup_expr="icontains")

    class Meta:
        model = Facility
        fields = "__all__"


@extend_schema(tags=["Sport_Facility"])
@extend_schema(description="Only allowed for User with is_owner=true", methods=["POST"])
class FacilityView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsTheOwnerOrAdmin]

    serializer_class = FacilitySerializer
    queryset = Facility.objects.all()

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = FacilityFilter

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


@extend_schema(tags=["Sport_Facility"])
@extend_schema(description="User must be the owner", methods=["GET"])
class FacilyUserView(generics.ListAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsTheOwner]

    serializer_class = FacilitySerializer
    queryset = Facility.objects.all()

    def get_queryset(self):
        user = self.request.user
        return Facility.objects.filter(user=user)


@extend_schema(tags=["Sport_Facility"])
@extend_schema(
    description="User must be the owner or admin", methods=["PATCH", "DELETE"]
)
@extend_schema(exclude=True, methods=["PUT"])
class FacilityDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsTheOwnerOrAdmin]

    serializer_class = DetailedFacilitySerializer
    queryset = Facility.objects.all()
    lookup_url_kwarg = "sport_facility_id"

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        address_instance = instance.address

        if address_instance is not None:
            address_instance.delete()

        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
