from django.db import models

class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    postdate = models.DateTimeField(auto_now_add=True, blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('post', args=[str(self.id)])

