# Generated by Django 3.2.4 on 2021-09-28 16:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0022_usermodel_has_premium'),
        ('companies', '0020_position_photo'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='match',
            unique_together={('position', 'jobseeker', 'company')},
        ),
    ]
