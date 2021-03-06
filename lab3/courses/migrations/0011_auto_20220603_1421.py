# Generated by Django 3.2.3 on 2022-06-03 14:21

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0010_auto_20220603_1419'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='uploads/'),
        ),
        migrations.AddField(
            model_name='course',
            name='thumbnail',
            field=models.ImageField(upload_to='uploads/', blank=True, null=True)
        ),
    ]
