from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.index, name='home-page'),
    path('about', views.about, name='about'),
    path('sign-up', views.Sign_up.as_view(), name='sign-up'),
    path('include', include('django.contrib.auth.urls')),
]
