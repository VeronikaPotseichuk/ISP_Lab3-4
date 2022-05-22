from io import BytesIO
from PIL import Image
from django.core import files
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext as _


class UserProfile(AbstractUser):
    age = models.PositiveIntegerField(default=18,
                                      verbose_name='Возраст')
    image = models.ImageField(upload_to='users/',
                              default='default.png',
                              max_length=100,
                              verbose_name='Фото')
    thumbnail = models.ImageField(upload_to='users/',
                                  blank=True, null=True)
    is_teacher = models.BooleanField(default=False,
                                     verbose_name='Преподаватель')

