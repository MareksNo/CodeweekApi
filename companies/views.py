from django.core import exceptions
from django.utils.datastructures import MultiValueDictKeyError

from rest_framework import permissions, status, serializers
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import CompanyProfile, Position
from .serializers import CompanyProfileSerializer, PositionSerializer
from .permissions import IsEmployerOrReadOnly, IsPositionOwnerOrReadOnly

from core.models import Occupation



class CompanyProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, company_id=None):
        print(request.data)
        data = {}

        try:
            profile = CompanyProfile.objects.get(user=request.user.id)
        except CompanyProfile.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)

        serializer = CompanyProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            data = serializer.data
            data['success'] = True
            return Response(data=data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request, company_id=None):
        try:
            profile = CompanyProfile.objects.get(id=company_id)
        except CompanyProfile.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        
        serializer = CompanyProfileSerializer(profile)
       
        return Response(serializer.data)


class PositionListCreateView(ListCreateAPIView):
    queryset = Position.objects.all()
    permission_classes = [IsEmployerOrReadOnly]
    serializer_class = PositionSerializer
    filterset_fields = ['company', 'position_occupation', 'id', ]

    def create(self, request, *args, **kwargs):
        position_data = request.data

        try:
            company_profile = CompanyProfile.objects.get(user=request.user)
        except exceptions.ObjectDoesNotExist as ex:
            raise serializers.ValidationError({"detail": "User with this ID does not have a CompanyProfile"})


        try:
            position_occupation = Occupation.objects.get(id=position_data['position_occupation'])
        except exceptions.ObjectDoesNotExist as ex:
            raise serializers.ValidationError({"detail": "Invalid occupation ID"})
        except ValueError:
            raise serializers.ValidationError({"detail": "Provided occupation ID is not numeric"})
        except MultiValueDictKeyError:
            raise serializers.ValidationError({"detail": "No occupation ID has been provided"})
        except KeyError:
            raise serializers.ValidationError({"detail": "No position_occupation has been provided"})
        
        
        new_position = Position.objects.create(
            company=company_profile,
            position_occupation=position_occupation,
            position_info=position_data.get('position_info', 'No info'),
            position_tools=position_data.get('position_tools', 'N/A'),
            position_country=position_data.get('position_country', 'N/A'),
            position_city=position_data.get('position_city', 'N/A'),
            position_languages=position_data.get('position_languages', 'N/A'),
            position_requirements=position_data.get('position_requirements', 'N/A'),
            price_range=position_data.get('price_range', 'N/A'),
            contract_type=position_data.get('contract_type', 'N/A')

        )
        
        new_position.save()

        serializer = PositionSerializer(new_position)

        return Response(serializer.data)


class PositionRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = PositionSerializer
    permission_classes = [IsPositionOwnerOrReadOnly]
    queryset = Position.objects.all()
