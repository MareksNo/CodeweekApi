from django.urls import path

from .views import (
    CompanyProfileView,
    PositionListCreateView,
    PositionRetrieveUpdateDestroyView,
    MatchView,
    MatchListView,
    VerifyCompanyView
)

urlpatterns = [
    path('company_profile/<int:company_id>/', CompanyProfileView.as_view(), name='company_profile'),

    path('positions/list_create/', PositionListCreateView.as_view(), name='position_list'),
    path('positions/<int:pk>/', PositionRetrieveUpdateDestroyView.as_view(), name='position_view'),
    path('positions/match/', MatchView.as_view(), name='match_view'),
    path('positions/match/list_view/', MatchListView.as_view(), name='match_list_view'),
    path('verify/', VerifyCompanyView.as_view(), name='verify_company_view')
]   