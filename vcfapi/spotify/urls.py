from django.urls import path, include
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r"auth", views.SpotifyAuth, basename="auth")


urlpatterns = [
    # path('auth', views.SpotifyAuth().as_view()),
    # path('request_user_auth', views.SpotifyUserAuth.as_view())
]

urlpatterns += router.urls