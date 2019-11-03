from insta.models import Post
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
	class Meta:
		model = Post
		fields = ('author', 'title', 'posted_on')