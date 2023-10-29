from django.shortcuts import render
from rest_framework. views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action



from spotify import models as spotify_models
from spotify import serializers as spotify_serializers
from spotify import utils as spotify_utils




# Create your views here.


class SpotifyAuth(ModelViewSet):

    queryset = spotify_models.DummyDB.objects.all()
    serializer_class = spotify_serializers.DummySerializer

    def get_queryset(self):
        
        if self.request.user.is_authenticated:
            return self.queryset.all()
        else:
            return self.queryset.none()
        
    @action(methods=["get"], detail=False)
    def get_spotify_client_auth(self, request, pk=None):
        
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
    
    @action(methods=["get"], detail=False)
    def get_spotify_user_auth(self, request, pk=None):

        # if not request.user.is_authenticated:
        #     return Response(
        #         data={
        #             "status": "FAILED",
        #             "message": "Unauthorized user",
        #         },
        #         status=status.HTTP_401_UNAUTHORIZED
        #     )


        is_auth, access = spotify_utils.SpotifyAPI().request_user_authorization()
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
                "message": "Spotify authentication",
                "data": access
            },
            status=status.HTTP_200_OK
        )



