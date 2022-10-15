from rest_framework import serializers
from users.serializers import UserBaseInfoSerializer
from .models import Facility


class FacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ["id","name", "email", "phone_number", "address_id", "user"]
        read_only_fields = ["user"]


class DetailedFacilitySerializer(serializers.ModelSerializer):
    user = UserBaseInfoSerializer(read_only=True)
    class Meta:
        model = Facility
        fields = "__all__"
        depth = 1


class FacilityBaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ["name"]