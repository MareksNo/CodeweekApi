# Generated by Django 3.2.4 on 2021-08-26 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0013_rename_position_languages2_position_position_languages'),
    ]

    operations = [
        migrations.AddField(
            model_name='companyprofile',
            name='description',
            field=models.TextField(blank=True, max_length=2000),
        ),
        migrations.AddField(
            model_name='companyprofile',
            name='specialization',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]