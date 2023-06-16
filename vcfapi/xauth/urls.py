from django.db import router
from django.urls import path, include
from xauth import views as xauth_views
from rest_framework.routers import DefaultRouter


urlpatterns = [
    path("login/", xauth_views.JWTAuth.as_view()),
    path("logout/", xauth_views.JWTDestroy.as_view()),
    # path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]

# urlpatterns += router.urls
