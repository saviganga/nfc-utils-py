import os
import base64
import requests
from dotenv import load_dotenv
load_dotenv()
import json

class SpotifyAPI:

    def __init__(self) -> None:

        self.CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
        self.CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
        self.BASE_URL = 'https://accounts.spotify.com/api'

    def get_token(self):

        # define the url
        url = f"{self.BASE_URL}/token"

        # define headers
        HEADERS = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # set payload
        payload = {
            "grant_type": "client_credentials",
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET
        }

        try:
            resp = requests.post(url=url, data=payload, headers=HEADERS)
            if resp.status_code == 200:
                return True, resp.json().get('access_token')
            else:
                return False, resp.json().get('error_description')

        except Exception as spotify_login_error:
            return False, "Server error"




