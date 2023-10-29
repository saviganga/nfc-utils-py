from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from rest_framework import routers
from . import views


urlpatterns = [
    path('spotify_callback', views.SpotifyWebhook().as_view()),
    # path('request_user_auth', views.SpotifyUserAuth.as_view())
]