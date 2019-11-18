from django.shortcuts import render, get_object_or_404, redirect
from .models import BlogPost, Tag
from django.conf import settings
from django.contrib.auth import get_user_model

def index(request):
    posts = BlogPost.objects.all()
    tags = Tag.objects.all()
    return render(request, 'mainapp/index.html', {'posts':posts, 'tags':tags})

def post(request, id):
    post = get_object_or_404(BlogPost, pk=id)
    return render(request, 'mainapp/post.html', {'object': post})

def tag_posts(request, name):
    name = name.lower()
    try:
        tag = Tag.objects.get(name=name)
        posts = tag.posts.all()
    except:
        posts = []
    title = "Posts about {}".format(name)

    return render(request, 'mainapp/filtered_post_list.html', {'posts':posts, 'title':title})

def user_posts(request, id):
    user = get_object_or_404(get_user_model(), pk=id)
    title = "Posts by {}".format(user.username)
    user_post_list = user.posts.all()
    return render(request, 'mainapp/filtered_post_list.html', {'posts':user_post_list, 'title':title})
