from django.urls import path
from django.http import JsonResponse
from .views import UserDetailView, UserListCreateView, PostDetailView, PostlistCreateView, FollowView, FeedView


urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user_list_create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('posts/', PostlistCreateView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('follow/<str:username>/', FollowView.as_view(), name='follow'),
    path('feed/', FeedView.as_view(), name='feed'),
]