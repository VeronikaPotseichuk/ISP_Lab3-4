import pytest
from django.db import models
from PIL import Image
from io import BytesIO
from django.core import files
from users.models import UserProfile
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ObjectDoesNotExist


class OrderField(models.PositiveIntegerField):
    def __init__(self, for_fields=None, *args, **kwargs):
        self.for_fields = for_fields
        super(OrderField, self).__init__(*args, **kwargs)

    def pre_save(self, model_instance, add):
        if getattr(model_instance, self.attname) is None:
            try:
                query_set = self.model.objects.all()
                if self.for_fields:
                    query = {field: getattr(model_instance, field)\
                             for field in self.for_fields}
                    query_set = query_set.filter(**query)
                last_item = query_set.latest(self.attname)
                value = last_item.order + 1
            except ObjectDoesNotExist:
                value = 0
            setattr(model_instance, self.attname, value)
            return value
        else:
            return super(OrderField, self).pre_save(model_instance, add)


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

    def __str__(self):
        return self.username

    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()
                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)
        thumb_io = BytesIO()
        img.save(thumb_io, 'svg', quality=85)
        thumbnail = files.File(thumb_io, name=image.name)
        return thumbnail

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


class Module(models.Model):
    course = models.ForeignKey(Course,
                               related_name='modules',
                               on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    order = OrderField(blank=True, for_fields=['course'])

    class Meta:
        verbose_name = 'Модуль'
        verbose_name_plural = 'Модули'
        ordering = ['order']

    def __str__(self):
        return '{}. {}'.format(self.order, self.title)


@pytest.fixture
def user_data():
    return dict(username='username',
                password='123123123!',
                email='email@email.ru',
                age=20,
                is_teacher=True)


@pytest.fixture
def user(user_data):
    return UserProfile.objects.create(**user_data)


@pytest.fixture
def authenticated_user(client, user_data):
    user = UserProfile.objects.create(**user_data)
    user.set_password(user_data.get('password'))
    user.save()
    client.login(**user_data)
    return user


@pytest.fixture
def subjects():
    return Subject.objects.create(title='subject',
                                  slug='subject')


@pytest.fixture
def course_data(authenticated_user, subjects):
    return dict(
        owner=authenticated_user,
        subject=subjects,
        title='course',
        slug='slug'
    )


@pytest.fixture
def courses(course_data):
    return Course.objects.create(**course_data)


@pytest.fixture
def module_data(courses):
    return dict(
        course=courses,
        title='module'
    )


@pytest.fixture
def modules(module_data):
    return Module.objects.create(**module_data)

