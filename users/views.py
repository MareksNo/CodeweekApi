from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import RegistrationSerializer, JobSeekerProfileSerializer

from rest_framework.authtoken.models import Token

class RegistrationView(APIView):
    def post(self, request, format=None):
        serializer = RegistrationSerializer(data=request.data)
        data = {}
        if serializer.is_valid():
            user = serializer.save()
            data['response'] = 'New user registered successfully!'
            data['email'] = user.email
            data['username'] = user.username
            data['is_employer'] = user.is_employer
            data['last_name'] = user.last_name
            data['first_name'] = user.first_name

            token = Token.objects.get(user=user)
            data['token'] = token.key
        else:
            data = serializer.errors
        return Response(data)


class JobSeekerProfileView(APIView):
    def get(self, request, pk, format=None):
        serializer = JobSeekerProfileSerializer()
        return Response(serializer.data)
