from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from apps.identity.serializers import RegisterSerializer
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from apps.identity.api.serializers import (
    LoginSerializer, CurrentUserSerializer, LogoutSerializer, UpdateCurrentUserSerializer, ChangePasswordSerializer,
    PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)
from rest_framework_simplejwt import tokens
from apps.identity.services import (
    generate_password_reset_token, send_password_reset_email,
)

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

    def patch(self, request):
        serializer = UpdateCurrentUserSerializer(
            request.user,
            data=request.data,
            partial=True
        )

        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        response_serializer = CurrentUserSerializer(user)
        return Response({
            "user": response_serializer.data
        },
        status=HTTP_200_OK,
        )

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = LogoutSerializer(
            data=request.data
        )

        serializer.is_valid(
            raise_exception=True
        )

        serializer.save()

        return Response(
            {
                "message": "Logout successful."
            },
            status=HTTP_200_OK,
        )

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(
            data=request.data,
            context={
                "request": request
            }
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                "message": "Password changed successfully."
            }
        )

class PasswordResetRequestView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        result = generate_password_reset_token(email)
        if result:
            send_password_reset_email(
                result["user"],
                result["token"],
            )
            return Response(
                {
                    "message": (
                        "If the email address exists, "
                        "password-reset instructions will be sent."
                    )
                },
                status=HTTP_200_OK,
            )

class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(
            data = request.data
        )

        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        new_password = serializer.validated_data["new_password"]

        user.set_password(new_password)
        user.save(update_fields=["password"])

        return Response(
            {
                "message": "Passoword has been reset successfully."
            },
            status=HTTP_200_OK,
        )
