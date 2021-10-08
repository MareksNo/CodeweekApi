from django.db import models

from django.contrib.postgres.fields import ArrayField
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db.models.signals import post_save
from django.dispatch import receiver


from core.models import Occupation
import users.models as user_models


class CompanyProfile(models.Model):
    user = models.OneToOneField("users.UserModel", on_delete=models.CASCADE, related_name="company_profile") 

    company_name = models.CharField(max_length=100, blank=True, null=True, unique=True)
    position = models.CharField(max_length=70, blank=True, default='')
    phone_number = models.CharField(max_length=20, blank=True, default='')
    logo = models.ImageField(upload_to='company_photos/', blank=True, default="/default_images/company_default.jpg")
    background_photo = models.ImageField(upload_to='company_photos/', blank=True, default="/default_images/jobseeker_default_background.jpg")
    country = models.CharField(max_length=20, blank=True, default='')
    company_size = models.CharField(max_length=30, blank=True, default='')
    country = models.TextField(max_length=900, blank=True)
    city = models.TextField(max_length=200, blank=True)
    description = models.TextField(max_length=2000, blank=True)
    specialization = models.CharField(max_length=500, blank=True)
    website_url = models.CharField(max_length=200, blank=True, default='')

    is_verified = models.BooleanField(max_length=200, blank=True, default=False)

    def __str__(self):
        return f'{self.company_name}\'s Company profile'

    @receiver(post_save, sender="users.UserModel")
    def create_user_profile(sender, instance, created, **kwargs):
        if instance.is_employer:
            if created:
                CompanyProfile.objects.create(user=instance)

    @receiver(post_save, sender="users.UserModel")
    def save_user_profile(sender, instance, **kwargs):
        if instance.is_employer:
            try:
                instance.company_profile.save()
            except ObjectDoesNotExist:
                CompanyProfile.objects.create(user=instance)


class Position(models.Model):
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE, related_name='positions')

    position_occupation = models.ForeignKey(Occupation, on_delete=models.SET_NULL, null=True, related_name="positions")
    position_info = models.TextField(max_length=20000)
    position_tools = models.CharField(max_length=500)
    position_city = models.CharField(max_length=300)
    position_country = models.CharField(max_length=250)
    position_languages = ArrayField(models.CharField(max_length=200), blank=True, default=list)
    position_requirements = models.TextField(max_length=20000)
    price_range = models.CharField(max_length=200)
    contract_type = models.TextField(max_length=1000)
    post_time = models.DateTimeField(auto_now_add=True)

    photo = models.ImageField(upload_to='company_photos/', blank=True)

    def __str__(self):
        if self.position_occupation:
            occupation_title = self.position_occupation.title
        else:
            occupation_title = None
        return f'{self.company.company_name}: {occupation_title}' 



class Match(models.Model):
    jobseeker = models.ForeignKey(user_models.JobSeekerProfile, on_delete=models.CASCADE)
    company = models.ForeignKey(CompanyProfile, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    jobseeker_accepted = models.BooleanField(null=True)
    company_accepted = models.BooleanField(null=True)

    matched = models.BooleanField(default=False)

    class Meta:
        unique_together = ('position', 'jobseeker', 'company')

    def __str__(self):
        return f'Position id {self.position.id}: Jobseeker: {self.jobseeker.user.email}, Company {self.company.company_name}'

    def clean(self):
        if not self.company == self.position.company:
            raise ValidationError("Please make sure that the company profile matches the position")
        return super().clean()
        