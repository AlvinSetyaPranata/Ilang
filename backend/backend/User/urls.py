from django.urls import path
from .views import (
    UserView, UserRegisterView, UserLoginView
    
)


urlpatterns = [
    path('users/', UserView.as_view(), name="get_user_view"),
    path('users/register/', UserRegisterView.as_view(), name="user_register_view"),
    path('users/login/', UserLoginView.as_view(), name="user_login_view")

]
