# Generated by Django 3.2.4 on 2021-07-26 12:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_occupationcategory_options'),
        ('users', '0005_alter_jobseekerprofile_profession_aka_activity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joboffer',
            name='job_title',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='job_offers', to='core.occupation'),
        ),
    ]
