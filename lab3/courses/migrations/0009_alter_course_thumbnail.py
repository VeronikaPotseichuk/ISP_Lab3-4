# Generated by Django 3.2.3 on 2022-06-01 21:46

from django.db import migrations
from django.db import models


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0008_alter_course_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='thumbnail',
            field=models.ImageField(upload_to='uploads/', blank=True, null=True)
        ),
    ]
