from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import permissions

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import RegistrationSerializer, JobSeekerProfileSerializer
from .models import JobSeekerProfile


class RegistrationView(APIView):
    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'New user registered successfully!'
            data['email'] = user.email
            data['is_employer'] = user.is_employer
            data['last_name'] = user.last_name
            data['first_name'] = user.first_name
            data['id'] = user.id

            token = Token.objects.get(user=user)
            data['token'] = token.key
        else:
            data = serializer.errors
        return Response(data)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        return Response({'token': token.key, 'id': token.user_id})


class JobSeekerProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, user_id=None):
        data = {}

        try:
            profile = JobSeekerProfile.objects.get(user=request.user.id)
        except JobSeekerProfile.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

        serializer = JobSeekerProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data['success'] = True
            return Response(data=data)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request, user_id=None):
        try:
           profile = JobSeekerProfile.objects.get(user=user_id)
        except JobSeekerProfile.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

        serializer = JobSeekerProfileSerializer(profile)
        return Response(serializer.data)


# class CompanyProfileView(APIView):
#     parser_classes = [MultiPartParser, FormParser]
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def put(self, request, user_id=None):
#         print(request.data)
#         data = {}

#         try:
#             profile = CompanyProfile.objects.get(user=request.user.id)
#         except CompanyProfile.DoesNotExist:
#             return Response(status.HTTP_404_NOT_FOUND)

#         serializer = CompanyProfileSerializer(profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             data = serializer.data
#             data['success'] = True
#             return Response(data=data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#     def get(self, request, user_id=None):
#         try:
#             profile = CompanyProfile.objects.get(user=user_id)
#         except CompanyProfile.DoesNotExist:
#             return Response(status.HTTP_404_NOT_FOUND)
        
#         serializer = CompanyProfileSerializer(profile)
#         return Response(serializer.data)
