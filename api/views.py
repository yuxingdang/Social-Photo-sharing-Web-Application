from django.shortcuts import render

# Create your views here.
from insta.models import Post
from rest_framework import generics
from .serializers import PostSerializer

class PostAPIView(generics.ListAPIView):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
