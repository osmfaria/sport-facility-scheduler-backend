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


class CourtView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsFacilityOwnerOrReadOnly]

    queryset = Court.objects.all()
    serializer_class = CourtSerializer

    lookup_url_kwarg = "facility_id"


    def perform_create(self, serializer):
        facility_id = self.kwargs[self.lookup_url_kwarg]
        facility = get_object_or_404(Facility,id=facility_id)

        return serializer.save(sport_facility=facility)

    def get_queryset(self):
        facility_id = self.kwargs[self.lookup_url_kwarg]
        facility = get_object_or_404(Facility,id=facility_id)
        
        return Court.objects.filter(sport_facility=facility)


class CourtDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsFacilityOwnerOrAdmin]

    queryset = Court.objects.all()
    serializer_class = CourtSerializer

    lookup_url_kwarg = "court_id"


class CourtAvailableSchedulesView(generics.RetrieveAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Court.objects.all()
    serializer_class = CourtAvailableSchedulesSerializers
    
    lookup_url_kwarg = "court_id"


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


class DeleteNonOperantingDay(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCourtOwnerOrReadOnly]

    queryset = NonOperatingDay.objects.all()
    serializer_class = NonOperatingDaysSerializer
    
    lookup_url_kwarg = "non_operanting_day_id"


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


class DeleteHolidayView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsCourtOwnerOrReadOnly]

    queryset = Holiday.objects.all()
    serializer_class = HolidaySerializer
    
    lookup_url_kwarg = "holiday_id"
