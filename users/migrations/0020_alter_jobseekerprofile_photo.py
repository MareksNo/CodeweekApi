# Generated by Django 3.2.4 on 2021-09-14 16:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0019_rename_skills2_joboffer_skills'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobseekerprofile',
            name='photo',
            field=models.ImageField(blank=True, default='/static/images/users/profile_default.jpg/', upload_to='user_photos/'),
        ),
    ]
