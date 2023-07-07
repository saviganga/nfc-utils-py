from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework import routers
from . import views


urlpatterns = [
    path('auth', views.SpotifyAuth().as_view()),
]