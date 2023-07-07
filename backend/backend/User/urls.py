from django.urls import path
from .views import (
    PostView, UserRegisterView, UserLoginView
    
)


urlpatterns = [
    path('posts/', PostView.as_view(), name="get_user_view"),
    path('users/register/', UserRegisterView.as_view(), name="user_register_view"),
    path('users/login/', UserLoginView.as_view(), name="user_login_view")

]
