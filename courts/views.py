from django.shortcuts import get_object_or_404
from facilities.models import Facility
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from courts.models import Court, Holiday, NonOperatingDay
from .permissions import IsFacilityOwnerOrAdmin, IsFacilityOwnerOrReadOnly, IsCourtOwnerOrReadOnly
from courts.serializers import (CourtAvailableSchedulesSerializers,
                                CourtSerializer, HolidaySerializer,
                                NonOperatingDaysSerializer)
from django_filters import rest_framework as filters
from utils.court_available_hours import list_court_available_hours
import datetime
from drf_spectacular.utils import extend_schema


class CourtFilter(filters.FilterSet):
    sport = filters.CharFilter(field_name="sport", lookup_expr="icontains")
    capacity = filters.NumberFilter(field_name="capacity", lookup_expr="gte")

    class Meta:
        model = Court
        fields = "__all__"


@extend_schema(tags=['Court'])

class CourtFilterView(generics.ListAPIView):

    queryset = Court.objects.all()
    serializer_class = CourtSerializer

    lookup_url_kwarg = ["city", "date"]

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CourtFilter


    def get_queryset(self):
        city = self.kwargs["city"].lower()
        date = datetime.datetime.strptime(self.kwargs["date"], "%Y-%m-%d")
        courts = Court.objects.filter(sport_facility__address__city = city)

        available_courts_id = [court.id for court in courts if type(list_court_available_hours(date, court)) == list]
        available_courts = Court.objects.filter(id__in=available_courts_id)

        return available_courts


@extend_schema(tags=['Court'])
@extend_schema(description='Only allowed for User with is_owner=true', methods=["POST"])


class CourtView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsFacilityOwnerOrReadOnly]

    queryset = Court.objects.all()
    serializer_class = CourtSerializer

    lookup_url_kwarg = "facility_id"

    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CourtFilter


    def perform_create(self, serializer):
        facility_id = self.kwargs[self.lookup_url_kwarg]
        facility = get_object_or_404(Facility,id=facility_id)

        return serializer.save(sport_facility=facility)


    def get_queryset(self):
        facility_id = self.kwargs[self.lookup_url_kwarg]
        facility = get_object_or_404(Facility,id=facility_id)
        
        return Court.objects.filter(sport_facility=facility)

@extend_schema(tags=['Court'])
@extend_schema(description='User must be the owner or admin', methods=["PATCH", "PUT", "DELETE"])

class CourtDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsFacilityOwnerOrAdmin]

    queryset = Court.objects.all()
    serializer_class = CourtSerializer

    lookup_url_kwarg = "court_id"


@extend_schema(tags=['Court'])

class CourtAvailableSchedulesView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

    queryset = Court.objects.all()
    serializer_class = CourtAvailableSchedulesSerializers
    
    lookup_url_kwarg = "court_id"


@extend_schema(tags=['Court'])
@extend_schema(description='User must be the owner or admin', methods=["POST"])

class RegisterNonOperantingDay(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCourtOwnerOrReadOnly]

    queryset = NonOperatingDay.objects.all()
    serializer_class = NonOperatingDaysSerializer
    
    lookup_url_kwarg = "court_id"


    def perform_create(self, serializer):
        court_id = self.kwargs[self.lookup_url_kwarg]
        court = get_object_or_404(Court,id=court_id)

        serializer.save(court=court)


@extend_schema(tags=['Court'])
@extend_schema(description='User must be the owner or admin', methods=["DELETE"])

class DeleteNonOperantingDay(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCourtOwnerOrReadOnly]

    queryset = NonOperatingDay.objects.all()
    serializer_class = NonOperatingDaysSerializer
    
    lookup_url_kwarg = "non_operanting_day_id"


@extend_schema(tags=['Court'])
@extend_schema(description='User must be the owner or admin', methods=["POST"])

class RegisterHolidayView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCourtOwnerOrReadOnly]

    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    
    lookup_url_kwarg = "court_id"


    def perform_create(self, serializer):
        court_id = self.kwargs[self.lookup_url_kwarg]
        court = get_object_or_404(Court,id=court_id)

        serializer.save(court=court)


@extend_schema(tags=['Court'])
@extend_schema(description='User must be the owner or admin', methods=["DELETE"])

class DeleteHolidayView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCourtOwnerOrReadOnly]

    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    
    lookup_url_kwarg = "holiday_id"
