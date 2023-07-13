from django.urls import path, re_path
from .views import (
    PostLostView, UserRegisterView, UserLoginView, AddPostView, PostFoundView
    
)


urlpatterns = [
    path('post/lost', PostLostView.as_view(), name="get_posts_view"),
    path('post/found', PostFoundView.as_view(), name="get_posts_view"),
    path('post/create/', AddPostView.as_view(), name="add_posts_view"),
    path('user/register/', UserRegisterView.as_view(), name="user_register_view"),
    path('user/auth/', UserLoginView.as_view(), name="user_login_view")
]
