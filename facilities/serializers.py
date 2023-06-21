from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from addresses.models import Address
from addresses.serializers import AddressSerializer
from users.serializers import UserBaseInfoSerializer
from utils.google_address import get_google_address

from .models import Facility


class FacilityBaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ["id", "name"]


class FacilitySerializer(serializers.ModelSerializer):
    from courts.serializers import CourtByFacilitySerializer

    address = AddressSerializer()
    user = UserBaseInfoSerializer(read_only=True)
    courts = CourtByFacilitySerializer(many=True, read_only=True)

    class Meta:
        model = Facility
        fields = ["id", "name", "email", "phone_number", "address", "user", "courts"]
        read_only_fields = ["user", "courts"]
        depth = 2

    def create(self, validated_data):
        address = validated_data.pop("address")
        repeated_address = Address.objects.filter(**address).exists()

        if repeated_address:
            raise ValidationError({"address": "address already exists."})

        map_address = get_google_address(address)

        address_instance = Address.objects.create(**address, map_image=map_address)
        facility = Facility.objects.create(**validated_data, address=address_instance)

        return facility


class DetailedFacilitySerializer(serializers.ModelSerializer):
    user = UserBaseInfoSerializer(read_only=True)
    address = AddressSerializer()

    class Meta:
        model = Facility
        fields = "__all__"
        depth = 1
    
    
