from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from spotify import utils as spotify_utils
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings



class SpotifyWebhook(APIView):

    def get(self, request, *args, **kwargs):


        code = request.query_params.get('code')

        is_token, token = spotify_utils.SpotifyAPI().request_user_access_token(code=code)
        if not is_token:
            print('here')
            return redirect(f'{settings.FE_REDIRECT_URL}/spotify/error')
        # return Response(
        #     data={
        #         "status": "SUCCESS",
        #         "message": "Spotify authentication",
        #         "data": token
        #     },
        #     status=status.HTTP_200_OK
        # )
        print('there')
        return redirect(f'{settings.FE_REDIRECT_URL}/spotify/success')
        





