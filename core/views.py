from rest_framework import permissions
from rest_framework.generics import ListAPIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from.permissions import IsAdminOrReadOnly

from .serilaizers import CEDOccupationCategorySerializer, OccupationSerializer, RetrieveOccupationCategorySerializer
from .models import Occupation, OccupationCategory

class CEDOccupationCategoryViewSet(ModelViewSet):
    permission_classes = [IsAdminUser]
    serializer_class = CEDOccupationCategorySerializer
    queryset = OccupationCategory.objects.all()


class OccupationViewSet(ModelViewSet):
    permission_classes = [IsAdminOrReadOnly]
    serializer_class = OccupationSerializer
    queryset = Occupation.objects.all()


class RetrieveOccupationsView(ListAPIView):
    filterset_fields = ['id', 'title']
    serializer_class = RetrieveOccupationCategorySerializer
    queryset = OccupationCategory.objects.all()
