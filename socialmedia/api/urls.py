from django.urls import path
from .views import UserDetailView, UserListCreateView, PostDetailView, PostlistCreateView, FollowView, FeedView


urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user_list_create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user_detail'),
    path('pots/', PostlistCreateView.as_view(), name='post_list_create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post_detail'),
    path('follow/<int:pk>/', FollowView.as_view(), name='follow'),
    path('feed/', FeedView.as_view(), name='feed'),
]