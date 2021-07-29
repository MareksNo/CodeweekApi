from django.urls import path

from .views import (
    RegistrationView,
    JobSeekerProfileView,
    CustomObtainAuthToken,
    JobOfferListCreateView,
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', CustomObtainAuthToken.as_view(), name='login'),
    path('jsprofile/<int:profile_id>/', JobSeekerProfileView.as_view(), name='jsprofile'),
    path('joboffers/list_create/', JobOfferListCreateView.as_view(), name='joboffer_list')

]   

# JobOffer Create/Edit/Retrieve/delete (Simmilar to Positions)
# User model view, edit/retrieve
