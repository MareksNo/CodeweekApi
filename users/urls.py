from django.urls import path

from .views import (
    RegistrationView,
    JobSeekerProfileView,
    CustomObtainAuthToken
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', CustomObtainAuthToken.as_view(), name='login'),
    path('jsprofile/<int:profile_id>/', JobSeekerProfileView.as_view(), name='jsprofile'),

]   

# JobOffer Create/Edit/Retrieve/delete (Simmilar to Positions)
# User model view, edit/retrieve
