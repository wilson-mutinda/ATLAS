from django.conf import settings
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthCheckAPIView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        return Response({
            "status": "ok",
            "application": "Atlas Business Suite",
            "version": "0.1.0",
            "environment": "development" if settings.DEBUG else "production",
        })