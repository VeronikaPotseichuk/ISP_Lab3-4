from django.db import models
from PIL import Image
from io import BytesIO
from django.core import files
from users.models import UserProfile


class Subject(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'
        ordering = ['title']

    def __str__(self):
        return self.title

class Course(models.Model):
    owner = models.ForeignKey(UserProfile,
                              related_name='courses_created',
                              on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,
                                related_name='courses',
                                on_delete=models.CASCADE)
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    overview = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    users = models.ManyToManyField(UserProfile,
                                   related_name='courses_joined',
                                   blank=True)
    image = models.ImageField(upload_to='uploads/',
                              blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/',
                                  blank=True, null=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ['-created']

    def __str__(self):
        return self.title

    def get_image(self):
        if self.image:
            return self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return self.thumbnail.url
            else:
                return ''

    @staticmethod
    def make_thumbnail(image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)
        thumbnail = files.File(thumb_io, name=image.name)
        return thumbnail
