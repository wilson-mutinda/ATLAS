from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status

from rest_framework.permissions import AllowAny

from apps.identity.serializers import RegisterSerializer

class RegisterAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):

        serializer = RegisterSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        return Response({
            "message": "User registered successfully.",
            "user": {
                "id": user.id,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
            },
        },
        status=status.HTTP_201_CREATED,)


class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        return Response({
            "message": "Login endpoint"
        })