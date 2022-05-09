from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='starting_page'),
    path('about', views.about, name='about'),

]
