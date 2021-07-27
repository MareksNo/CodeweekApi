from django.urls import path

from .views import (
    RegistrationView,
    JobSeekerProfileView,
    CustomObtainAuthToken
)

urlpatterns = [
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', CustomObtainAuthToken.as_view(), name='login'),
    path('jsprofile/<int:user_id>/', JobSeekerProfileView.as_view(), name='jsprofile'),

]   

# JobOffer Create/Edit/Retrieve/delete (Simmilar to Positions)
# Job Seeker Profile Edit/Retrieve (Simmilar to Company Profile)
# User model view, edit/retrieve
