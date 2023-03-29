from rest_framework.exceptions import ValidationError
from rest_framework import serializers
from addresses.models import Address
from users.serializers import UserBaseInfoSerializer
from .models import Facility
from addresses.serializers import AddressSerializer, AddressBaseSerializer
from utils.google_address import get_google_address


class FacilitySerializer(serializers.ModelSerializer):
    address = AddressSerializer()
    user = UserBaseInfoSerializer(read_only=True)


    class Meta:
        model = Facility
        fields = ["id","name", "email", "phone_number", "address", "user"]
        read_only_fields = ["user"]


    def create(self, validated_data):
        address = validated_data.pop("address")

        repeated_address = Address.objects.filter(**address).exists()

        if repeated_address:
            raise ValidationError({"detail": "address already exists."})

        map_address = get_google_address(address)

        address_instance = Address.objects.create(**address, map_image=map_address)
        facility = Facility.objects.create(**validated_data, address=address_instance)

        return facility

        
class DetailedFacilitySerializer(serializers.ModelSerializer):
    user = UserBaseInfoSerializer(read_only=True)

    class Meta:
        model = Facility
        fields = "__all__"
        depth = 1


class FacilityBaseInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Facility
        fields = ["id", "name"]