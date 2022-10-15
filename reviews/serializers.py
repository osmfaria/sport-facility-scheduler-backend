from rest_framework import serializers
from .models import Review
from users.serializers import UserBaseInfoSerializer
from courts.serializers import CourtInfoForReviewSerializer


class ReviewSerializer(serializers.ModelSerializer):
    user = UserBaseInfoSerializer(read_only=True)
    court = CourtInfoForReviewSerializer(read_only=True)
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = ["court", "user"]
