from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import authenticate
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.permissions import  AllowAny, IsAuthenticated
from rest_framework.pagination import PageNumberPagination 
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import UserRegisterSerializer, PostsAddSerializers, PostsGetSerializers, UserSerializer
from .models import Post
from .authentication import LoginAuthentication, MainAuthentication
from backend.settings import DEBUG
from .utils import reactjs_request_unpack
from .pagination import PostPagination





class PostFoundView(ListAPIView):
    class Meta:
        ordering = ['date_created']


    queryset = Post.objects.all()
    pagination_class = PostPagination
    serializer_class = PostsGetSerializers


    def get_queryset(self):
        return self.queryset.filter(founded=True)


class PostLostView(ListAPIView):
    class Meta:
        ordering = ['date_created']


    queryset = Post.objects.all()
    pagination_class = PostPagination
    serializer_class = PostsGetSerializers


    def get_queryset(self):
        return self.queryset.filter(founded=False)





class AddPostView(APIView):
    permission_classes = (IsAuthenticated,)
    authentication_classes = (MainAuthentication,)

    def post(self, req):
        post_data = req.POST.copy()


        user_id = MainAuthentication().get_user_id(req)["user_id"]
        post_data["user"] = user_id


        serializer = PostsAddSerializers(data=post_data)

        if not serializer.is_valid(raise_exception=DEBUG):
            return Response({"messege" : "Authentication Fail"}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer.save()


        return Response({"message" : "Data Has Been Created"}, status=status.HTTP_201_CREATED)


    
class UserLoginView(APIView):
    """
    Login from unauthenticated users
    """

    permission_classes = (AllowAny,)
    authentication_classes = (LoginAuthentication,)


    def post(self, req):
        post_data = reactjs_request_unpack(req)
        

        if not "username" in post_data:
            return Response(status=status.HTTP_404_NOT_FOUND)


        model = get_user_model()

        authenticate(req)


        user = model.objects.filter(username=post_data["username"])
        
        if not user:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        user = user.get()


        if not req.user.is_authenticated:
            # User doesnt have token but authenticated successfully

            token = RefreshToken.for_user(user)

            data = {
                "message" : "Authentication Success",
                "access" : str(token.access_token),
                "refresh" : str(token),
                "data" : UserSerializer(user).data
            }

            res = Response(data, status=status.HTTP_200_OK)
            res["Access-Control-Allow-Origin"] = "*"

            return res
        

        return Response()



class UserRegisterView(APIView):
    """
    User registration view
    """
    permission_classes = (AllowAny,)


    def post(self, req):
        post_data = reactjs_request_unpack(req)

        serialiezer = UserRegisterSerializer(data=post_data)


        if not serialiezer.is_valid(raise_exception=DEBUG):
            return Response({"message" : "Register Fail"}, status=status.HTTP_400_BAD_REQUEST)

        serialiezer.save()
        
        res = Response({"message" : "Register Success"}, status=status.HTTP_201_CREATED)
        res["Access-Control-Allow-Origin"] = "*"

        return res
