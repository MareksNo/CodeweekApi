from django.urls import path

from .views import (
    CompanyProfileView,
    PositionListCreateView,
    PositionRetrieveUpdateDestroyView
)

urlpatterns = [
    path('company_profile/<int:company_id>/', CompanyProfileView.as_view(), name='company_profile'),

    path('positions/list_create/', PositionListCreateView.as_view(), name='position_list'),
    path('positions/<int:pk>/', PositionRetrieveUpdateDestroyView.as_view(), name='position_view')
]   