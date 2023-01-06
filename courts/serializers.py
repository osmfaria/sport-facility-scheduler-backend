from datetime import datetime
from rest_framework import serializers
from courts.models import Court
from courts.models import Court, Holiday, NonOperatingDay
from utils.court_available_hours import list_court_available_hours
from facilities.serializers import FacilityBaseInfoSerializer


def get_week_day(day):
    days_of_the_week = ["MONDAY", "TUESDAY", "WEDNESDAY", "THURSDAY", "FRIDAY", "SATURDAY", "SUNDAY"]

    return days_of_the_week[day]


class CourtSerializer(serializers.ModelSerializer):
    sport_facility = FacilityBaseInfoSerializer(read_only=True)
    class Meta:
        model = Court
        fields = "__all__"
        read_only_fields = ["sport_facility"]


class CourtInfoForScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Court
        fields = [ "name", "price_by_hour"]

class CourtInfoForReviewSerializer(serializers.ModelSerializer):
    sport_facility = FacilityBaseInfoSerializer(read_only=True)
    class Meta:
        model = Court
        fields = [ "name", "sport_facility"]


class NonOperatingDaysSerializer(serializers.ModelSerializer):
    class Meta:
        model = NonOperatingDay
        fields = "__all__"
        read_only_fields = ["court"]
    

class HolidaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Holiday
        fields = "__all__"
        read_only_fields = ["court"]


class CourtAvailableSchedulesSerializers(serializers.ModelSerializer):
    available_hours = serializers.SerializerMethodField()

    class Meta:
        model = Court
        fields = ["name", "available_hours", "price_by_hour"]


    def get_available_hours(self, obj):
        input_str = self.context.get('request').parser_context.get('kwargs').get('date')
        input_date = datetime.strptime(input_str, '%Y-%m-%d')
        return list_court_available_hours(input_date, obj)
        