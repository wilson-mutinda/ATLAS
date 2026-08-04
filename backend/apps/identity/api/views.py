from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from apps.identity.serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from apps.identity.api.serializers import (
    LoginSerializer, CurrentUserSerializer
)
from rest_framework_simplejwt import tokens

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response(
            {
                "message": "User registered successfully.",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            },
            status = HTTP_201_CREATED,
        )

class LoginAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(
            data=request.data,
            context={
                "request": request
            },
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        refresh = tokens.RefreshToken.for_user(user)
        return Response(
            {
                "message": "Login successful.",
                "access": str(refresh.access_token),
                "refresh": str(refresh),
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                },
            },
            status= HTTP_200_OK,
        )

class CurrentUserAPIView(APIView):
    def get(self, request):
        serializer = CurrentUserSerializer(request.user)

        return Response(
            {
                "user": serializer.data,
            },
            status=HTTP_200_OK,
        )
    