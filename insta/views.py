from django.shortcuts import render
from annoying.decorators import ajax_request

# Create your views here.
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse, reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
#from django.contrib.auth.forms import UserCreationForm

from insta.forms import CustomUserCreationForm
from insta.models import Post, Like, Comment, InstaUser, UserConnection

class HelloWorld(TemplateView):
	template_name = 'test.html'

class PostsView(ListView):
	model = Post 
	template_name = 'index.html' 

	def get_queryset(self):
		current_user = self.request.user
		following = set()
		if self.request.user.is_authenticated:
			for conn in UserConnection.objects.filter(creator=current_user).select_related('following'):
				following.add(conn.following)
		return Post.objects.filter(author__in=following)

class PostDetailView(DetailView):
	model = Post 
	template_name = 'post_detail.html'

class UserDetailView(DetailView):
	model = InstaUser 
	template_name = 'user_detail.html'  

class PostCreatelView(LoginRequiredMixin, CreateView):
	model = Post 
	template_name = 'post_create.html'
	fields = '__all__'  
	login_url = 'login'

class PostUpdatelView(UpdateView):
	model = Post 
	template_name = 'post_update.html'
	fields = '__all__' 

class ProfileEditlView(UpdateView):
	model = InstaUser  
	template_name = 'edit_profile.html'
	fields = '__all__'  

class PostDeletelView(DeleteView):
	model = Post 
	template_name = 'post_delete.html'
	success_url = reverse_lazy("posts") 

class Signup(CreateView):
	form_class = CustomUserCreationForm
	template_name = 'signup.html'
	success_url = reverse_lazy("login") 

class ExploreView(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'explore.html'
    login_url = 'login'

    def get_queryset(self):
        return Post.objects.all().order_by('-posted_on')[:20]


@ajax_request
def addLike(request):
	post_pk = request.POST.get('post_pk')
	post = Post.objects.get(pk=post_pk)
	try:
		like = Like(post=post, user=request.user)
		like.save()
		result = 1
	except Exception as e:
		like = Like.objects.get(post=post, user=request.user)
		like.delete()
		result = 0

	return {
		'result': result,
		'post_pk': post_pk
	}


@ajax_request
def addComment(request):
	comment_text = request.POST.get('comment_text')
	post_pk = request.POST.get('post_pk')
	post = Post.objects.get(pk=post_pk)
	commenter_info = {}

	try:
		comment = Comment(comment=comment_text, user=request.user, post=post)
		comment.save()

		username = request.user.username

		commenter_info = {
			'username': username,
			'comment_text': comment_text
		}

		result = 1
	except Exception as e:
		print(e)
		result = 0

	return {
		'result': result,
		'post_pk': post_pk,
		'commenter_info': commenter_info
	}

@ajax_request
def toggleFollow(request):
	current_user = InstaUser.objects.get(pk=request.user.pk)
	follow_user_pk = request.POST.get('follow_user_pk')
	follow_user = InstaUser.objects.get(pk=follow_user_pk)

	try:
		if current_user != follow_user:
			if request.POST.get('type') == 'follow':
				connection = UserConnection(creator=current_user, following=follow_user)
				connection.save()
			elif request.POST.get('type') == 'unfollow':
				UserConnection.objects.filter(creator=current_user, following=follow_user).delete()
			result = 1
		else:
			result = 0
	except Exception as e:
		print(e)
		result = 0

	return {
		'result': result,
		'type': request.POST.get('type'),
		'follow_user_pk': follow_user_pk
	}




