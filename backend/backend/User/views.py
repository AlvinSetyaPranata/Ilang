from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import authenticate
from rest_framework import status
from rest_framework.permissions import  AllowAny, IsAuthenticated
from .serializers import UserRegisterSerializer


# Create your views here.
class UserView(APIView):
    def get(self, req):
        # get user from given id
        post_data = req.POST

        print(post_data)

        return Response()
    
    
class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, req):
        post_data = req.POST

        model = get_user_model()

        # Authenticate
        d = authenticate()

        return Response()



class UserRegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, req):
        post_data = req.POST

        print(post_data)

        serialiezer = UserRegisterSerializer(data=post_data)


        if not serialiezer.is_valid(raise_exception=True):
            return Response()



        serialiezer.save()

        return Response()