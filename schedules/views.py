from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import Response, status
from utils.court_available_hours import list_court_available_hours
from utils.set_new_hour import set_new_hour
from datetime import datetime
from courts.models import Court
from schedules.models import Schedule
from schedules.serializers import ScheduleSerializer
from .permissions import IsFacilityOwner, IsOwnerOrFacilityOwnerOrAdmin
from .functions import sendmail


class ScheduleCreateView(generics.ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsFacilityOwner]

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    lookup_url_kwarg = "court_id"

    def create(self, request, *args, **kwargs):
        court_id = self.kwargs[self.lookup_url_kwarg]
        court = Court.objects.get(id=court_id)
        
        username = request.user.username.capitalize()
        input_date_str = request.data["datetime"]
        number_of_hours = request.data["number_of_hours"]
        
        datetime_obj = datetime.strptime(input_date_str, '%Y-%m-%d %H:00')
        available_hours = list_court_available_hours(datetime_obj, court)

        starting_hour = datetime_obj.hour
        final_hour = datetime_obj.hour + number_of_hours
        schedule_hours_list = [hour for hour in range(starting_hour, final_hour)]

        is_available = all(elem in available_hours for elem in schedule_hours_list)

        if not is_available:
            message = {
                "detail": "Schedule period not available. Please check the available hours"
            }
            return Response(message, status=status.HTTP_406_NOT_ACCEPTABLE)

        schedule_hours_list.reverse()

        for hour in schedule_hours_list:

            date_str = set_new_hour(input_date_str, hour)

            serializer = self.get_serializer(
                data={"datetime": date_str, "number_of_hours": number_of_hours}
            )
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)


        sendmail(
            subject=f"Hey {username} your appointment is confirmed",
            recipient=[request.user.email],
            court=court,
            duration=number_of_hours,
            date_time=datetime_obj,
            user=username,
            template="schedule.html"
        )

        headers = self.get_success_headers(serializer.data)
        
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


    def perform_create(self, serializer):
        court_id = self.kwargs[self.lookup_url_kwarg]
        court = get_object_or_404(Court, id=court_id)

        serializer.save(user=self.request.user, court=court)


    def get_queryset(self):
        court_id = self.kwargs[self.lookup_url_kwarg]
        court = get_object_or_404(Court, id=court_id)

        return Schedule.objects.filter(court=court)


class CancelScheduleView(generics.DestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrFacilityOwnerOrAdmin]

    queryset = Schedule.objects.all()
    serializer_class = ScheduleSerializer

    lookup_url_kwarg = "schedule_id"


    def destroy(self, request, *args, **kwargs):
        schedule_id = self.kwargs[self.lookup_url_kwarg]
        schedule = Schedule.objects.get(id=schedule_id)

        self.check_object_permissions(self.request, schedule)

        schedule_hour = schedule.datetime.hour
        last_schedule_hour = schedule_hour + (schedule.number_of_hours - 1)

        schedules_hours = Schedule.objects.filter(
            user=schedule.user,
            datetime__hour__range=(schedule_hour, last_schedule_hour),
        )

        for instance in schedules_hours:
            self.perform_destroy(instance)

        username = schedule.user.first_name.capitalize()
        
        sendmail(
        subject=f"Hey {username}, Your appointment has been canceled",
        recipient=[schedule.user.email],
        court=schedule.court,
        duration=schedule.number_of_hours,
        date_time=schedule.datetime,
        user=username,
        template="cancelation.html"
        )

        return Response(status=status.HTTP_204_NO_CONTENT)



