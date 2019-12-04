---
% Django Models - Blog Posts Module
% Will Holderness
---



# Module - Posts

## Create Model class

#### Create BlogPost Model in mainapp/models.py

````class BlogPost(models.Model):```

#### Import settings so we can access `AUTH_USER_MODEL`

`from  django.conf  import  settings`

#### Add author foreign key

Add ForeignKey called author with model as settings.AUTH_USER_MODEL, related_name as "posts", and on_delete set to models.CASCADE.

#### Add title CharField

Add a models.CharField called `title`, set max_length parameter to 200

#### Add `body` TextField

Add a models.TextField called `body`

#### Add `postdate` DateTimeField

Add a models.DateTimeField. Set auto_now_add parameter to true, and blank parameter to True

#### Implement str() method to simplify rendering in admin view and templates.

```python
def str(self):
	return self.title
```

#### Implement get_absolute_url function

`from django.urls import reverse`

```python
def get_absolute_url(self):
	return reverse('post', args=[str(self.id)])
```

#### (Final model:)

```python     
from django.db import models
from django.urls import reverse
from django.conf import settings

class BlogPost(models.Model):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="posts",
        on_delete=models.CASCADE,
    )
    title = models.CharField(max_length=200)
    body = models.TextField()
    postdate = models.DateTimeField(auto_now_add=True, blank=True)
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post', args=[str(self.id)])
```
## Regist BlogPost to Admin Site

#### Add BlogPost model to admin.py

```python
from .models import BlogPost

admin.site.register(BlogPost)
```
## Update views.py in mainapp

#### Import BlogPost model from .models.

#### Import get_object_or_404 from django.shortcuts

## Update index view to grab data from BlogPost model.

#### Get posts from BlogPosts model

Set `posts` variable to `BlogPosts.objects.all()`

#### Update `post` view using shortcut function.

Replace try accept block with get_object_or_404()

```post = get_object_or_404(BlogPost, pk=id)```

set `post` variable to the BlogPost returned by `get_object_or_404(BlogPost, pk=id)` 

#### (Final Views.py)

```python
from django.shortcuts import render, get_object_or_404
from .models import BlogPost

def index(request):
    posts = BlogPost.objects.all()
    return render(request, 'mainapp/index.html', {'posts':posts})

def post(request, id):
    post = get_object_or_404(BlogPost, pk=id)
    return render(request, 'mainapp/post.html', {'post': post})

```

## Migrate to new schema

#### Make migrations and migrate.

```bash
python manage.py makemigrations
python manage.my migrate
```

#### Create some posts from terminal

_Fill me in_

# Module - Tags

#### Add Tag model to models.py

```python
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
```

#### Add clean method to sanitize input.

```python
    def clean(self):
        self.name = self.name.lower()
```

#### Add __str__ method to prettify and make life easier.

```python
    def __str__(self):
        return self.name
```

#### Add many to many relationship to BlogPost model for tags.

```python
    tags = models.ManyToManyField('Tag', related_name='posts')
```

#### Add get_absolute_url method to enable us to access tag page by model reference.

```python
    def get_absolute_url(self):
        return reverse('tag_posts', args=[str(self.name)])
```

#### Uncomment tag section of index and post templates

Remove `<!-- -->` tags from both index and post templates.

#### Add post by tag view to mainapp/views.py

```python
def tag_posts(request, name):
    name = name.lower()
    try:
        tag = Tag.objects.get(name=name)
        posts = tag.posts.all()
    except:
        posts = []
    title = "Posts about {}".format(name)

    return render(request, 'mainapp/filtered_post_list.html', {'posts':posts, 'title':title})
```

#### Add tag path and new view to mainapp/urls.py

```python
    path('tag/<str:name>', views.tag_posts, name='tag_posts'),
```

#### Add tags to admin.py

```python
from .models import BlogPost, Tag
admin.site.register(Tag)
```

#### Add default value to migration for each post.

TBD

#### Make migrations and migrate.

```bash
python manage.py makemigrations
python manage.my migrate
```

