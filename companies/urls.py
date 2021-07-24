from django.urls import path

from .views import (
    CompanyProfileView,
    PositionListCreateView,
)

urlpatterns = [
    path('company_profile/<int:user_id>/', CompanyProfileView.as_view(), name='company_profile'),
    path('positions/list_create/', PositionListCreateView.as_view(), name='position_list')
]   