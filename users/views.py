from django.core import exceptions
from django.utils.datastructures import MultiValueDictKeyError
from django.contrib.auth import get_user_model

from rest_framework import generics, serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework import permissions

from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken

from .serializers import RegistrationSerializer, JobSeekerProfileSerializer, JobOfferSerializer, UserSerializer
from .models import JobOffer, JobSeekerProfile
from .permissions import IsJobSeekerOrReadOnly, IsJobOfferOwnerOrReadOnly, UserIsOwnerOrReadOnly

from companies.models import Occupation, CompanyProfile
from companies.serializers import CompanyProfileSerializer



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

            if user.is_employer:
                data['profile_id'] = CompanyProfile.objects.get(user=user).id
            else:
                data['profile_id'] = JobSeekerProfile.objects.get(user=user).id

            token = Token.objects.get(user=user)
            data['token'] = token.key
        else:
            data = serializer.errors
        return Response(data)


class UserView(generics.RetrieveUpdateDestroyAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserIsOwnerOrReadOnly]

    def get(self, request, pk, *args, **kwargs):
        data = {}

        User = get_user_model()
        try:
           user = User.objects.get(id=pk)
        except User.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)


        serializer = UserSerializer(user)
        data = serializer.data

        if user.is_employer:
            profile = user.company_profile
            data['profile'] = CompanyProfileSerializer(profile).data
        else:
            profile = user.jobseeker_profile
            data['profile'] = JobSeekerProfileSerializer(profile).data

        return Response(data)


class CustomObtainAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super(CustomObtainAuthToken, self).post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])

        data = {}

        User = get_user_model()
        user = User.objects.get(id=token.user_id)

        data['user_id'] = user.id
        data['token'] = token.key

        try:
            if user.is_employer:
                profile = user.company_profile
                
            else:
                profile = user.jobseeker_profile
        except User.jobseeker_profile.RelatedObjectDoesNotExist:
            return Response({"detail": "JobSeekerProfile does not exist for this user"}, status=status.HTTP_400_BAD_REQUEST)
        except User.company_profile.RelatedObjectDoesNotExist:
            return Response({"detail": "CompanyProfile does not exist for this user"}, status=status.HTTP_400_BAD_REQUEST)
        
        data['is_employer'] = user.is_employer
        data['profile'] = profile.id
        

        return Response(data)


class JobSeekerProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, profile_id=None):
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

    def get(self, request, profile_id=None):
        try:
           profile = JobSeekerProfile.objects.get(id=profile_id)
        except JobSeekerProfile.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

        serializer = JobSeekerProfileSerializer(profile)
        return Response(serializer.data)


# Needs testing
class JobOfferListCreateView(generics.ListCreateAPIView):
    queryset = JobOffer.objects.all()
    permission_classes = [IsJobSeekerOrReadOnly]
    serializer_class = JobOfferSerializer
    filterset_fields = ['user_profile', 'id', 'job_title']

    def create(self, request, *args, **kwargs):
        joboffer_data = request.data

        try:
            profile = JobSeekerProfile.objects.get(user=request.user)
        except exceptions.ObjectDoesNotExist:
            raise serializers.ValidationError({"detail": "JobSeeker profile not found for current user"})

        
        try:
            job_title = Occupation.objects.get(id=joboffer_data['job_title'])
        except exceptions.ObjectDoesNotExist as ex:
            raise serializers.ValidationError({"detail": "Invalid occupation ID"})
        except ValueError:
            raise serializers.ValidationError({"detail": "Provided occupation ID is not numeric"})
        except MultiValueDictKeyError:
            raise serializers.ValidationError({"detail": "No occupation ID has been provided"})
        except KeyError:
            raise serializers.ValidationError({"detail": "No job title has been provided"})



        new_job_offer = JobOffer.objects.create(
            user_profile=profile,
            job_title=job_title,
            info=joboffer_data.get('info', 'No info'),
            skills=joboffer_data.get('skills', 'N/A'),
            contract_type=joboffer_data.get('contract_type', 'N/A'),
            knowledge=joboffer_data.get('knowledge', 'N/A'),
        )
        
        new_job_offer.save()

        serializer = JobOfferSerializer(new_job_offer)

        return Response(serializer.data)


class JobOfferRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = JobOfferSerializer
    permission_classes = [IsJobOfferOwnerOrReadOnly]
    queryset = JobOffer.objects.all()
