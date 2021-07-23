from django.contrib import admin
from .models import Occupation, OccupationCategory

admin.site.register(OccupationCategory)
admin.site.register(Occupation)
