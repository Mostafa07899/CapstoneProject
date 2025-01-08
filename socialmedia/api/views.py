from django.shortcuts import render
from rest_framework import generics, permissions, status, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, User, Follower
from .serializers import UserSerializer, FollowerSerializer, PostSerializer


# Create your views here.

#user crud
class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


#post crud
class PostlistCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, *args, **kwargs):
        post = self.get_object()
        if post.user != request.user:
            return Response({'error': 'you can only delete your own posts.'}, status=status.HTTP_403_FORBIDDEN)
        return super().delete(request, *args, **kwargs)
    

#follow/unfollow
class FollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        user_to_follow = User.objects.all()
        if user_to_follow == request.user:
            return Response({'error': 'you can not follow yourself'}, status=status.HTTP_400_BAD_REQUEST)
        
        Follower.objects.get_or_create(user=user_to_follow, follower=request.user)
        return Response({'done!': 'you are now following this person'}, status=status.HTTP_201_CREATED)
    
    def delete(self, request, user_id):
        user_to_unfollow = User.objects.get(id=user_id)
        Follower.objects.filter(user=user_to_unfollow, follower=request.user).delete()
        return Response({'done!': 'you have unfollowed this user'}, status=status.HTTP_204_NO_CONTENT)
    

#feed
class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        following = request.user.following.all()
        posts = Post.objects.filter(user__in=[f.user for f in following]).order_by('-timestamp')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)
    
#sub views
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class FollowerViewSet(viewsets.ModelViewSet):
    queryset = Follower.objects.all()
    serializer_class = FollowerSerializer

