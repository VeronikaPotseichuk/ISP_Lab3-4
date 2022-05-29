from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from courses.views import CourseListView
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
     path('',
          CourseListView.as_view(),
          name='course_list'),
     path('accounts/login/',
          auth_views.LoginView.as_view(),
          name='login'),
     path('accounts/logout/',
          auth_views.LogoutView.as_view(),
          name='logout'),
     path('accounts/password_reset/',
          auth_views.PasswordResetView.as_view(),
          name='password_reset_form'),
     path('accounts/password_reset/confirm/',
          auth_views.PasswordResetConfirmView.as_view(),
          name='password_reset_confirm'),
     path('admin/', admin.site.urls),
     path('course/', include('courses.urls')),
     path('users/', include('users.urls')),
     path('users/', include('django.contrib.auth.urls')),
     path('api/', include('courses.api.urls', namespace='api')),
     path('api/drf/auth/', include('rest_framework.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
