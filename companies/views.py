from datetime import date
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import CompanyProfile
from .serializers import CompanyProfileSerializer


class CompanyProfileView(APIView):
    def put(self, request, user_id):
        try:
            profile = CompanyProfile.objects.get(user=user_id)
        except CompanyProfile.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        
        serializer = CompanyProfileSerializer(profile, data=request.data)
        data = {}
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data['success'] = True
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, user_id):
        try:
            profile = CompanyProfile.objects.get(user=user_id)
        except CompanyProfile.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        
        serializer = CompanyProfileSerializer(profile)
        return Response(serializer.data)
