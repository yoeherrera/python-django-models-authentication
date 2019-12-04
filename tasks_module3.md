

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
