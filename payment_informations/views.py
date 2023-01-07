from rest_framework import generics
from .models import PaymentInformation
from .serializers import PaymentInformationSerializer
from .permissions import IsAuthenticated, IsOwner
from rest_framework.authentication import TokenAuthentication
from drf_spectacular.utils import extend_schema

@extend_schema(tags=['Payments'])

class PaymentInformationView(generics.CreateAPIView):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated, IsOwner] 
        
        queryset= PaymentInformation.objects.all()
        serializer_class = PaymentInformationSerializer
        

        def perform_create(self, serializer):
                serializer.save(user=self.request.user)


@extend_schema(tags=['Payments'])

class ListUserPaymentInformations(generics.ListAPIView):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated, IsOwner] 
        
        queryset= PaymentInformation.objects.all()
        serializer_class = PaymentInformationSerializer
        lookup_url_kwarg = "user_id"


        def get_queryset(self):
                return PaymentInformation.objects.filter(user=self.request.user)


@extend_schema(tags=['Payments'])

class PaymentDetailView(generics.RetrieveDestroyAPIView):
        authentication_classes = [TokenAuthentication]
        permission_classes = [IsAuthenticated, IsOwner] 
        
        queryset= PaymentInformation.objects.all()
        serializer_class = PaymentInformationSerializer
        lookup_url_kwarg = "payment_id"

