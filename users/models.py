from django.utils.translation import gettext_lazy

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

from django.core.exceptions import ObjectDoesNotExist

from django.core.validators import MaxValueValidator

from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token

from core.models import Occupation

class CustomAccountManager(BaseUserManager):
    def create_user(self, email, password, **other_fields):
        if not email:
            raise ValueError(gettext_lazy('You must provide an email address'))


        email = self.normalize_email(email)
        user = self.model(email=email, **other_fields)

        user.set_password(password)
        user.save()

        return user
    

    def create_superuser(self, email, password, **other_fields):
        other_fields.setdefault('is_staff', True)
        other_fields.setdefault('is_superuser', True)
        other_fields.setdefault('is_active', True)

        if other_fields.get('is_staff') is not True:
            raise ValueError(
                'Superuser must be assigned to is_staff=True'
            )
        if other_fields.get('is_superuser') is not True:
            raise ValueError(
                'Superuser must be assigned to is_superuser=True'
            )
        return self.create_user(email, password, **other_fields)


class UserModel(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(gettext_lazy('email address'), unique=True)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    date_joined = models.DateTimeField(gettext_lazy('date joined'), auto_now_add=True)

    is_employer = models.BooleanField()
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True) # Can be used for email validation 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['is_employer']

    objects = CustomAccountManager()

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class JobSeekerProfile(models.Model):
    user = models.OneToOneField(UserModel, on_delete=models.CASCADE, related_name="jobseeker_profile")

    photo = models.ImageField(upload_to='user_photos/', blank=True)
    birth_date = models.CharField(max_length=40, blank=True)
    location = models.TextField(max_length=900, blank=True)
    interests = models.TextField(max_length=3000, default='', blank=True)
    experience = models.TextField(max_length=3000, default='', blank=True)
    languages = models.TextField(max_length=1500, default='', blank=True)
    knowledge = models.TextField(max_length=3000, default='', blank=True)
    extra = models.TextField(max_length=3000, default='', blank=True)

    profession_aka_activity = models.ForeignKey(Occupation, on_delete=models.SET_NULL, null=True, related_name="job_seekers")

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}\'s JobSeeker profile'

    @receiver(post_save, sender=UserModel)
    def create_user_profile(sender, instance, created, **kwargs):
        if not instance.is_employer:
            if created:
                JobSeekerProfile.objects.create(user=instance)

    @receiver(post_save, sender=UserModel)
    def save_user_profile(sender, instance, **kwargs):
        if not instance.is_employer:
            try:
                instance.jobseeker_profile.save()
            except ObjectDoesNotExist:
                JobSeekerProfile.objects.create(user=instance)


class JobOffer(models.Model):
    user_profile = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='job_offers')

    job_title = models.ForeignKey(Occupation, on_delete=models.SET_NULL, null=True, related_name="job_offers")
    skills = models.CharField(max_length=300, blank=True)
    knowledge = models.TextField(max_length=3000, blank=True)
    info = models.TextField(max_length=2000, blank=True)
    contract_type = models.CharField(max_length=25, blank=True)
    post_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.job_title.title}'


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
