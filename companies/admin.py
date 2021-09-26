from django.contrib import admin
from .models import Match, Position, CompanyProfile

admin.site.register(Position)
admin.site.register(CompanyProfile)
admin.site.register(Match)
