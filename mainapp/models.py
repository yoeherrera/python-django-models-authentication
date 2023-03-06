from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
    
    def clean(self):
        return self.name.lower()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('tag_posts', args=[str(self.name)])
