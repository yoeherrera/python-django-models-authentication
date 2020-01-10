

#### Add Tag model to models.py
We want to be able to add tags to each post in order organize them better by topic.  To do that we'll create a new Tag mode..  Create the Tag model by adding a new class into `mainapp/models.py`. Name the class `Tag` and make it extend `models.Model`. In the class body, add a field called `name` and set it to `models.CharField()`. Pass it a `max_length` of `50`.
```python
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)
```

#### Add clean method to sanitize input.
We want all of the tags to be lowercase. To the `Tag` class, add a method named `clean` that will set `name` to lowercase.
```python
    def clean(self):
        self.name = self.name.lower()
```

#### Add __str__ method to make Tag objects readable
To the `Tag` class, add the following to string method:
```python
    def __str__(self):
        return self.name
```

#### Add many to many relationship to BlogPost model for tags.
Since we want tags to categorize posts by topic, we want to create a relationship between the `Tag` model and the `BlogPost` model.  In the `BlogPost` class, add `tags` as a field and set it equal to calling `models.ManyToManyField()` with `'Tag'` and `related_name='posts'` as parameters.
```python
    tags = models.ManyToManyField('Tag', related_name='posts')
```

#### Add view to display posts by tag to mainapp/views.py
We would like to display a Tag page that displays all of the posts with that Tag.  In order to do that, we need to create a view that will generate that page.  In `mainapp/views.py`, create a function `tag_posts(request, name)`.  Also return `render(request, 'mainapp/filtered_post_list.html')`.


```python
def tag_posts(request, name):
    return render(request, 'mainapp/filtered_post_list.html')
```

#### Pass title to template
We want to pass a title for Tag page to the template.  First, create a `name` variable and set it equal to `name.lower()` so we can ensure the tag is lowercase.  Then, create a `title` variable and set it equal to `"Posts about {}".format(name)`.
To pass the `title` to the template, add the following parameter to the end of the render() call, `{'title':title}`.

```python
def tag_posts(request, name):
    name = name.lower()
    title = "Posts about {}".format(name)

    return render(request, 'mainapp/filtered_post_list.html', {'posts':posts, 'title':title})
```

#### Find posts and pass to template
Since we want to display all of the posts with the name tag, let's first find the Tag object.  Call `Tag.objects.get(name=name)` and set that equal to a tag variable.  Then, get all of the posts with that tag by calling `tag.posts.all()` and setting the result equal to a variable named `posts`. Since the tag may not exist, wrap those 2 lines in try/except blocks.  In the except block, set `posts = []`.  Finally, pass the `posts` list to the template by adding `'posts':posts` to the dict in the `render()` call, `{'posts':posts, 'title':title}`.

```python
def tag_posts(request, name):
    name = name.lower()
    title = "Posts about {}".format(name)
    try:
        tag = Tag.objects.get(name=name)
        posts = tag.posts.all()
    except:
        posts = []
    

    return render(request, 'mainapp/filtered_post_list.html', {'posts':posts, 'title':title})
```

#### In Tag model add get_absolute_url() method 
To generate a url for the specified tag page, we can use django.urls reverse() function to generate the url from the view. Back in the `Tag` class, in `mainapp/models.py`, create a method `get_absolute_url(self)` that returns `reverse('tag_posts', args=[str(self.name)])`. Where `tag_posts` is the name of the view we just created. 
```python
    def get_absolute_url(self):
        return reverse('tag_posts', args=[str(self.name)])
```

#### Add tag path and new view to mainapp/urls.py

```python
    path('tag/<str:name>', views.tag_posts, name='tag_posts'),
```

#### Uncomment tag section of index and post templates

Remove `<!-- -->` tags from both index and post templates.

#### Add tags to admin.py

```python
from .models import BlogPost, Tag
admin.site.register(Tag)
```

#### Add Posts with tags (optional task)

TBD

#### Make migrations and migrate.

```bash
python manage.py makemigrations
python manage.my migrate
```
