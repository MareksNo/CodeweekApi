from django.urls import path
from django.urls.conf import include

from rest_framework import routers

from .views import (
    CEDOccupationCategoryViewSet,
    OccupationViewSet,
    RetrieveOccupationsView
)

router = routers.DefaultRouter()

router.register('occupations', OccupationViewSet)
router.register('occupation_categories', CEDOccupationCategoryViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('get_occupations/', RetrieveOccupationsView.as_view(), name='get_occupations')
]
