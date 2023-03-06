from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from django.urls import reverse

class User(AbstractUser):
    pass

class BlogPost(models.Model):
    title = models.CharField(max_length=200,unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,related_name="posts",on_delete=models.CASCADE)
    body = models.TextField()
    postdate = models.DateTimeField(auto_now_add=True,blank=True)
    tags = models.ManyToManyField('Tag', related_name="posts")
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("post",args=[str(self.id)]) 


