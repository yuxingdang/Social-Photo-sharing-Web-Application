from django.contrib import admin

from insta.models import Post, InstaUser, Like, Comment, UserConnection#, PostTwo

# Register your models here.
admin.site.register(Post)
admin.site.register(InstaUser)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(UserConnection)
#admin.site.register(PostTwo)
