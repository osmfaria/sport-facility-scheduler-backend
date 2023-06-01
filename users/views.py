from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView, Request, Response, status
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from users.functions import sendActivateEmail
from .token import AccountActivationTokenGenerator
from django.http import HttpResponse, HttpResponseRedirect
from users.models import User
from users.permissions import IsOwnerOrAdmin
from users.serializers import (LoginSerializer, UserDetailSerializer, UserSerializer)
from drf_spectacular.utils import extend_schema


@extend_schema(tags=['User'])

class ListUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
@extend_schema(tags=['User'])

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer



    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        user = User.objects.get(id=serializer.data["id"])
        
        sendActivateEmail(request, user=user, recipient=[user.email])

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


@extend_schema(description='Confirmation email must be activated before first login')

class LoginView(APIView):
    # added for auto generated documentation only
    serializer_class = LoginSerializer
    queryset = User.objects.all()
    # -------------------------------------------

    @extend_schema(tags=['User'])

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = authenticate(**serializer.validated_data)

        if user:
            token,_ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key, "user": user}, status.HTTP_200_OK)

        return Response({"detail": "invalid username or password"}, status.HTTP_400_BAD_REQUEST)


@extend_schema(tags=['User'])
@extend_schema(description='Must be the account owner or admin', methods=["DELETE", "PATCH", "PUT"])

class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrAdmin]
    
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_url_kwarg = 'user_id'




def activate(request, uidb64, token):
    account_activation_token = AccountActivationTokenGenerator()

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
    
        return HttpResponseRedirect("https://www.google.com/")

    else:
        return HttpResponse("Link expired")