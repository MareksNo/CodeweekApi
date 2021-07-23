# Generated by Django 3.2.4 on 2021-07-15 09:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CompanyProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(blank=True, max_length=100)),
                ('position', models.CharField(blank=True, default='', max_length=70)),
                ('phone_number', models.CharField(blank=True, default='', max_length=20)),
                ('logo', models.ImageField(blank=True, upload_to='company_photos/')),
                ('background_photo', models.ImageField(blank=True, upload_to='company_photos/')),
                ('country', models.CharField(blank=True, default='', max_length=20)),
                ('company_size', models.CharField(blank=True, default='', max_length=30)),
                ('location', models.TextField(blank=True, max_length=900)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Position',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_title', models.CharField(max_length=300)),
                ('position_info', models.TextField(max_length=20000)),
                ('position_tools', models.CharField(max_length=500)),
                ('position_location', models.CharField(max_length=300)),
                ('position_languages', models.CharField(max_length=400)),
                ('position_requirements', models.TextField(max_length=20000)),
                ('price_range', models.CharField(max_length=200)),
                ('contract_type', models.TextField(max_length=1000)),
                ('post_time', models.DateTimeField(auto_now_add=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='positions', to='companies.companyprofile')),
            ],
        ),
    ]
