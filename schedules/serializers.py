from rest_framework import serializers
from schedules.models import Schedule
from courts.serializers import CourtInfoForScheduleSerializer
from users.serializers import UserBaseInfoSerializer

class ScheduleSerializer(serializers.ModelSerializer):  
    court = CourtInfoForScheduleSerializer(read_only=True)  
    user = UserBaseInfoSerializer(read_only=True)
    class Meta:
        model = Schedule
        fields = ["id", "datetime", "number_of_hours",  "user", "court"]
        read_only_fields = ["user", "court"]

    