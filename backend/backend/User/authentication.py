import jwt
from rest_framework import authentication
from rest_framework.exceptions import (
    ParseError, AuthenticationFailed, NotFound
)
from django.contrib.auth import get_user_model
from backend.settings import SECRET_KEY     # on production use .env

# Move to .env on production
AUTHORIZATION_HEADER = "JWT" 
ALGORITHMS = ["HS256"]


class LoginAuthentication(authentication.BaseAuthentication):
     def auth_without_credentials(self, data):
        user = get_user_model().objects.filter(username=data["username"])

        if not user:
            raise NotFound("Pengguna tidak ditemukan")
        
        user = user[0]
        
        if not user.check_password(data["password"]):
            raise AuthenticationFailed("Kata Sandi salah")
        
        return None
     
     
     def authenticate(self, request):
        data = request.POST

        token = request.META.get('HTTP_AUTHORIZATION')

        if not token:
            return self.auth_without_credentials(data)
        

        token = token.replace(AUTHORIZATION_HEADER, "").strip()
        payload = ""

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHMS)

        except jwt.exceptions.InvalidSignatureError:
            raise AuthenticationFailed("Token Error")
        
        except ParseError:
            raise ParseError("Galat saat memeriksa token")
        
        except:
            pass


        user = get_user_model().objects.filter(username=data["username"])

        if not user or not user.check_password(data["password"]):
            raise AuthenticationFailed("Username atau Password salah")

             
        return user, payload
     



