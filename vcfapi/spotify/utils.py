import os
import base64
import requests
from dotenv import load_dotenv
load_dotenv()
import json
import string, random
from django.conf import settings


from userapp import models as user_models

class Utils:

    def generate_rand_state_str(self, n):
        res = ''.join(random.choices(string.ascii_letters, k=n))
        return res



class SpotifyAPI: 

    def __init__(self) -> None:

        self.CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
        self.CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET')
        self.BASE_URL = 'https://accounts.spotify.com'
        self.STATE = Utils().generate_rand_state_str(n=16)
        self.SCOPES = "user-read-playback-state user-modify-playback-state user-read-currently-playing playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public user-top-read user-read-recently-played user-library-read user-read-email user-read-private"
        self.REDIRECT_URI = settings.SPOTIFY_REDIRECT_URI

    def get_token(self):

        # define the url
        url = f"{self.BASE_URL}/api/token"

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
        
    
    def request_user_authorization(self):

        ''' https://developer.spotify.com/documentation/web-api/tutorials/code-flow '''

        # define the url 
        url = f"{self.BASE_URL}/authorize"

        HEADERS = {
            "Content-Type": "application/x-www-form-urlencoded"
        }

        # generate state and define scopes
        state = self.STATE
        scopes = self.SCOPES

        

        # define url query params
        params = {
            "client_id": self.CLIENT_ID,
            "response_type": "code",
            "redirect_uri": self.REDIRECT_URI,
            "state": state,
            "scope": scopes,
            "show_dialog": True
        }

        resp = requests.Request('GET', url=url, params=params).prepare().url
        return True, resp

    def request_user_access_token(self, code):

        client_id_message_bytes = self.CLIENT_ID.encode('ascii')
        client_id_base64_bytes = base64.b64encode(client_id_message_bytes)
        client_id_base64_message = client_id_base64_bytes.decode('ascii')

        client_secret_message_bytes = self.CLIENT_SECRET.encode('ascii')
        client_secret_base64_bytes = base64.b64encode(client_secret_message_bytes)
        client_secret_base64_message = client_secret_base64_bytes.decode('ascii')

        # HEADERS = {
        #     "Authorization": f"Basic {client_id_base64_message}:{client_secret_base64_message}",
        #     "Content-Type": "application/x-www-form-urlencoded"
        # }


        url = f'{self.BASE_URL}/api/token'

        payload = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": self.REDIRECT_URI,
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET
        }

        try:
            resp = requests.post(url=url, data=payload)
            if resp.status_code == 200:
                spotify_auth_info = {
                    "access_token": resp.json().get('access_token'),
                    "token_type": resp.json().get('token_type'),
                    "scope": resp.json().get('scope'),
                    "expires_in": resp.json().get('expires_in'),
                    "refresh_token": resp.json().get('refresh_token'),
                }
                
                # get user available devices
                is_available_devices, available_devices = self.get_user_available_devices(access_token=spotify_auth_info.get('access_token'))
                if not is_available_devices:
                    return False, 'No available devices'
                spotify_auth_info['available_devices'] = available_devices
                spotify_auth_info['selected_device'] = available_devices[0].get('id')

                # get user profile
                is_user, user_email = self.get_user_profile(access_token=spotify_auth_info.get('access_token'))
                if not is_user:
                    return False, user_email
                
                # print(user_email)

                try:
                    user = user_models.CustomUser.objects.get(email=user_email.get('email'))
                    user.spotify_auth = spotify_auth_info
                    user.save()
                    # print(user.spotify_auth)
                except Exception as user_error:
                    print(user_error)
                    user = user_models.CustomUser.objects.create(
                        user_name=user_email.get('display_name'),
                        email=user_email.get('email'),
                        first_name=user_email.get('display_name'),
                        last_name=user_email.get('display_name'),
                        spotify_auth=spotify_auth_info
                    )
                    return True, spotify_auth_info
                return True, spotify_auth_info
            else:
                print('hia')
                print(resp.json())
                return False, 'Unable to get user access token'
        except Exception as user_access_token_error:
            print(user_access_token_error)
            return False, "User access token error"
        
    def get_user_available_devices(self, access_token):

        url = "https://api.spotify.com/v1/me/player/devices/"

        HEADERS = {
            "Authorization": f"Bearer {access_token}",
            # "content-Type": "application/json"
        }

        try:
            resp = requests.get(url=url, headers=HEADERS)
            if resp.status_code == 200:
                # print(resp.json())
                return True, resp.json().get('devices')
            else:
                # print(resp.status_code)
                # print(resp.json())
                return False, 'error'
        except Exception as get_devices_error:
            print(get_devices_error)
            return False, 'device error'
        
    def get_user_profile(self, access_token):

        url = 'https://api.spotify.com/v1/me'

        HEADERS = {
            "Authorization": f"Bearer {access_token}",
            # "content-Type": "application/json"
        }

        try:
            resp = requests.get(url=url, headers=HEADERS)
            if resp.status_code == 200:
                print(resp.json())
                return True, resp.json()#.get('email')
            else:
                # print(resp.status_code)
                # print(resp.json())
                return False, 'error'
        except Exception as get_devices_error:
            print(get_devices_error)
            return False, 'user profile error'








