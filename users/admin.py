from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, BlogPost

admin.site.register(BlogPost)