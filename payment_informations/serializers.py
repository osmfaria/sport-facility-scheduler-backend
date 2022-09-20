from .models import PaymentInformation
from users.serializers import UserBaseInfoSerializer
from rest_framework.serializers import ModelSerializer


class PaymentInformationSerializer(ModelSerializer):
    user = UserBaseInfoSerializer(read_only=True)
    
    class Meta:
        model= PaymentInformation
        fields='__all__'
        read_only_fields = ["user"]
        depth = 1
