import jwt
from rest_framework import authentication
from rest_framework.exceptions import (
    ParseError, AuthenticationFailed, NotFound
)
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from backend.settings import SECRET_KEY     # on production use .env

# Move to .env on production
AUTHORIZATION_HEADER = "JWT" 
ALGORITHMS = ["HS256"]
SAFE_METHODS = ["GET"]


class LoginAuthentication(authentication.BaseAuthentication):
     def auth_without_credentials(self, req):

        data = req.POST

        user = get_user_model().objects.filter(username=data["username"])


        if not user:
            raise NotFound("Pengguna tidak ditemukan")
        
        user = user.get()
        
        
        if not user.check_password(data["password"]):
            raise AuthenticationFailed("Kata Sandi salah")
        

     
     def authenticate(self, request):
        data = request.POST

        if not data:
            return None

        token = request.META.get('HTTP_AUTHORIZATION')

        if not token:
            return self.auth_without_credentials(request)
        

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

        if not user: 
            raise AuthenticationFailed("Username atau Password salah")
        
        user = user.get()

        if not user.check_password(data["password"]):
            raise AuthenticationFailed("Username atau Password salah")

             
        return user, payload


     @classmethod
     def get_user(cls, user_id):
         user = get_user_model()

         try:
             return user.objects.get(pk=user_id)
         
         except user.DoesNotExist:
             return None


class MainAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        if request.method in SAFE_METHODS:
            return None

        payload = self.get_user_id(request)

        user_id = payload["user_id"]

        return self.get_user(user_id), payload
    
    
    @classmethod
    def get_user(cls, user_id):
         user = get_user_model()

         try:
             return user.objects.get(pk=user_id)
         
         except user.DoesNotExist:
             return None
         
    @classmethod
    def get_user_id(cls, request):
        data = request.POST

        if not data:
            return None

        token = request.META.get('HTTP_AUTHORIZATION')

        if not token:
            raise AuthenticationFailed("Unauthorized")
        

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

        return payload
