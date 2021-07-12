from django.contrib import admin
from .models import JobSeekerProfile, JobOffer, UserModel

admin.site.register(UserModel)
admin.site.register(JobSeekerProfile)
admin.site.register(JobOffer)
