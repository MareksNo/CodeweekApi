from django.urls import path
from rest_framework.fields import USE_READONLYFIELD

from .views import (
    RegistrationView,
    JobSeekerProfileView,
    CustomObtainAuthToken,
    JobOfferListCreateView,
    JobOfferRetrieveUpdateDestroyView,
    UserView,
    SelfUserView
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('user/<int:pk>/', UserView.as_view(), name='user_view'),
    path('user/', SelfUserView.as_view(), name='self_user_view'),
    path('login/', CustomObtainAuthToken.as_view(), name='login'),
    path('jsprofile/<int:profile_id>/', JobSeekerProfileView.as_view(), name='jsprofile'),
    path('joboffers/list_create/', JobOfferListCreateView.as_view(), name='joboffer_list'),
    path('joboffers/<int:pk>/', JobOfferRetrieveUpdateDestroyView.as_view(), name='joboffer_view'),


]   

# JobOffer Create/Edit/Retrieve/delete (Simmilar to Positions)
# User model view, edit/retrieve
