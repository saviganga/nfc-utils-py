from urllib import request
from django.utils import timezone
from django.contrib.auth.models import AnonymousUser
from xauth import exceptions as xauth_exceptions
from xauth import utils as xauth_utils
from rest_framework.authentication import BaseAuthentication


class JWTAuthentication(BaseAuthentication):
    def __init__(self, realm="API"):
        self.realm = realm

    def authenticate(self, request, **kwargs):
        """[Function to extract jwt token for an header]

        Arguments:
            request {[type] -- [description]}

        Returns:
            [token] -- [userobj]
        """
        try:
            auth_header = request.META.get("HTTP_AUTHORIZATION", None)
            if auth_header:
                # print(auth_header)
                auth_method, auth_token = auth_header.split(" ", 1)
                if not auth_token:
                    return None
                if not auth_method.lower() == "jwt":
                    return None
                user = JWTAuthentication.verify_access_token(auth_token)
                # print(user)
                return user, None
            else:
                print('anaon')
                return AnonymousUser(), None

        except Exception as e:
            print(e)
            pass

    def verify_access_token(auth_token):
        """[verify and decode the jwt token  provided]

        Arguments:
            auth_token {[token]} -- [jwt_token]

        Returns:
            [user] -- [user obj]
        """
        payload, user = xauth_utils.decode_jwt(auth_token)
        print(user)
        return user

