from django.core import exceptions

from rest_framework import permissions, status, serializers
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from .models import CompanyProfile, Position
from .serializers import CompanyProfileSerializer, PositionSerializer
from .permissions import IsEmployerOrReadOnly

from core.models import Occupation



class CompanyProfileView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def put(self, request, user_id=None):
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


    def get(self, request, user_id=None):
        try:
            profile = CompanyProfile.objects.get(user=user_id)
        except CompanyProfile.DoesNotExist:
            return Response(status.HTTP_404_NOT_FOUND)
        
        serializer = CompanyProfileSerializer(profile)
        return Response(serializer.data)


# Need for custom authentication for making sure that user is an owner of a company.
# Need for custom create, for passing the id of the company profile.
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


        new_position = Position.objects.create(
            company=company_profile,
            position_occupation=position_occupation,
            position_info=position_data['position_info'],
            position_tools=position_data['position_tools'],
            position_location=position_data['position_location'],
            position_languages=position_data['position_languages'],
            position_requirements=position_data['position_requirements'],
            price_range=position_data['price_range'],
            contract_type=position_data['contract_type']

        )
        
        new_position.save()

        serializer = PositionSerializer(new_position)

        return Response(serializer.data)

class PositionRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    pass
