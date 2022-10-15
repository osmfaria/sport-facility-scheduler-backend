from rest_framework import serializers
from django.utils.timezone import now
from .models import User
    

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email", "first_name", "last_name", "is_owner", "is_superuser", "date_joined", "is_active"]
        read_only_fields = ["date_joined", "is_active"]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data:dict) -> User:
        return User.objects.create_user(**validated_data)


class UserBaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class UserDetailSerializer(serializers.ModelSerializer):
    # schedules = ScheduleSerializer(many=True)
    current_schedules = serializers.SerializerMethodField()
    schedule_history = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ["id", "username", "email", "first_name", "last_name", "current_schedules", "schedule_history", "is_owner", "date_joined"]
        read_only_fields = ["current_schedules","schedule_history", "is_owner", "date_joined"]
    
    

    def get_schedule_history(self, obj):
        
        return [{"datetime" : schedule.datetime, "court" : schedule.court.name} for schedule in obj.schedules.all() if schedule.datetime < now()]

    def get_current_schedules(self, obj):
        
        return [{"datetime" : schedule.datetime, "court" : schedule.court.name} for schedule in obj.schedules.all() if schedule.datetime >= now()]
