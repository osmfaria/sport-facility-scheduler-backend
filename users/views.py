from django.contrib.auth import authenticate
from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView, Request, Response, status

from users.models import User
from users.permissions import IsOwnerOrAdmin
from users.serializers import (LoginSerializer, UserDetailSerializer,
                               UserSerializer)


class ListUsersView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class LoginView(APIView):
    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(**serializer.validated_data)

        if user:
            token,_ = Token.objects.get_or_create(user=user)
            return Response({"token": token.key}, status.HTTP_200_OK)

        return Response({"detail": "invalid username or password"}, status.HTTP_400_BAD_REQUEST)

class UserDetailsView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrAdmin]
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    lookup_url_kwarg = 'user_id'
