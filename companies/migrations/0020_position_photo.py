# Generated by Django 3.2.4 on 2021-09-28 15:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0019_auto_20210925_0939'),
    ]

    operations = [
        migrations.AddField(
            model_name='position',
            name='photo',
            field=models.ImageField(blank=True, upload_to='company_photos/'),
        ),
    ]
