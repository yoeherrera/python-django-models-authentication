from django.shortcuts import render, get_object_or_404
from .models import BlogPost

def index(request):
    posts = BlogPost.objects.all()
    return render(request, 'mainapp/index.html', {'posts':posts})

def post(request, id):
    post = get_object_or_404(BlogPost, pk=id)
    return render(request, 'mainapp/post.html', {'post': post})