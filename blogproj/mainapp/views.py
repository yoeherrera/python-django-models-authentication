from django.shortcuts import render, get_object_or_404
from .models import BlogPost, Tag

def index(request):
    posts = BlogPost.objects.all()
    tags = Tag.objects.all()
    return render(request, 'mainapp/index.html', {'posts':posts, 'tags':tags})

def post(request, id):
    post = get_object_or_404(BlogPost, pk=id)
    return render(request, 'mainapp/post.html', {'post': post})

def tag(request, name):
    name = name.lower()
    try:
        tag = Tag.objects.get(name=name)
        posts = tag.posts.all()
    except:
        posts = []

    return render(request, 'mainapp/tag.html', {'posts':posts, 'tag':name})
