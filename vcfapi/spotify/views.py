from django.shortcuts import render
from rest_framework. views import APIView
from rest_framework.response import Response
from rest_framework import status, generics

from spotify import models as spotify_models
from spotify import serializers as spotify_serializers
from spotify import utils as spotify_utils


# Create your views here.


class SpotifyAuth(APIView):

    queryset = spotify_models.DummyDB.objects.all()
    serializer_class = spotify_serializers.DummySerializer

    def get(self, request):

        is_auth, access = spotify_utils.SpotifyAPI().get_token()
        if not is_auth:
            return Response(
                data={
                    "status": "FAILED",
                    "message": access,
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            data={
                "status": "SUCCESS",
                "message": "Spotify authentication successful",
                "data": {"access": access}
            },
            status=status.HTTP_200_OK
        )



    
       



