from django.shortcuts import render
from django.conf import settings
from django.http import Http404

from datetime import datetime
ALL_POSTS = [
 {
    'id':0,
    'author': {'username':'will', 'id':'1'},
    'title':'My first blog post',
    'body': 'This is my first post. I hope you like it.',
    'postdate': datetime(2019, 10, 1),
    'get_absolute_url': '/blog/post/0'
 },
 {
    'id':1,
    'author': {'username':'will', 'id':'1'},
    'title':'My second blog post',
    'body': 'I\'ve got tons of these now. This is fun.',
    'postdate': datetime(2019, 10, 2),
    'get_absolute_url': '/blog/post/1'
 },
]

def index(request):
    posts = ALL_POSTS
    return render(request, 'mainapp/index.html', {'posts':posts})

def post(request, id):
    try:
        post = ALL_POSTS[id]
    except IndexError:
        raise Http404("Post does not exist")
    return render(request, 'mainapp/post.html', {'object': post})
