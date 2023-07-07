from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import authenticate
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination 
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer, PostsSerializers, PostsGetSerializers
from .models import Post
from .authentication import LoginAuthentication, MainAuthentication
from backend.settings import DEBUG


# Create your views here.
class PostView(ListAPIView):
    queryset = Post.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = PostsGetSerializers



class AddPostView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MainAuthentication,)

    def post(self, req):
        post_data = req.POST.copy()


        user_id = MainAuthentication().get_user_id(req)["user_id"]
        post_data["user"] = user_id

        serializer = PostsSerializers(data=post_data)

        if not serializer.is_valid(raise_exception=DEBUG):
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()


        return Response(status=status.HTTP_201_CREATED)


    
class UserLoginView(APIView):
    """
    Login from unauthenticated users
    """

    permission_classes = (AllowAny,)
    authentication_classes = (LoginAuthentication,)


    def post(self, req):
        post_data = req.POST

        model = get_user_model()

        # Authenticate       
        if not "username" in post_data and not "password" in post_data:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        authenticate(req)


        user = get_user_model().objects.filter(username=post_data["username"])
        
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user = user.get()


        if not req.user.is_authenticated:
            # User doesnt have token but authenticated successfully

            token = RefreshToken.for_user(user)

            data = {
                "access" : str(token.access_token),
                "refresh" : str(token)
            }

            return Response(data, status=status.HTTP_202_ACCEPTED)
        

        return Response()



class UserRegisterView(APIView):
    """
    User registration view
    """
    permission_classes = (AllowAny,)


    def post(self, req):
        post_data = req.POST

        serialiezer = UserRegisterSerializer(data=post_data)


        if not serialiezer.is_valid(raise_exception=DEBUG):
            return Response(status=status.HTTP_400_BAD_REQUEST)

        serialiezer.save()

        return Response(status=status.HTTP_201_CREATED)
