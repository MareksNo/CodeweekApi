from django.urls import path

from .views import (
    CompanyProfileView,
)

urlpatterns = [
    path('company_profile/<int:user_id>/', CompanyProfileView.as_view(), name='company_profile')
]   