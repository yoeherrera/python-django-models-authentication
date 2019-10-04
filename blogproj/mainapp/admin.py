from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import BlogPost, Tag

admin.site.register(BlogPost)
admin.site.register(Tag)