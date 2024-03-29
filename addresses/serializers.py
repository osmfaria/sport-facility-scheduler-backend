from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = "__all__"
        read_only_fields = ['map_image']


class AddressBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["street", "number", "city", "state", "zipcode"]



