from django.urls import path
from .views import (
    PostView, UserRegisterView, UserLoginView, AddPostView
    
)


urlpatterns = [
    path('posts/', PostView.as_view(), name="get_posts_view"),
    path('posts/add/', AddPostView.as_view(), name="add_posts_view"),
    path('user/register/', UserRegisterView.as_view(), name="user_register_view"),
    path('user/auth/', UserLoginView.as_view(), name="user_login_view")
]
