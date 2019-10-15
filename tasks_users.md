# Module - Users
#### Create user app

`python manage.py startapp users`

#### Add `users` app to settings.py `INSTALLED_APPS`

```python
INSTALLED_APPS = [
    ...
    'mainapp',
    'users'
]
```



#### Copy registration templates into new folder `templates` inside user app.

#### Create custom User model in `models.py`

* import AbstractUser from django.contrib.auth.models
* create new class `User` and derive from AbstractUser
* Leave class definition empty with `pass` The base class has all we need for now.

```python
from django.db import models
from django.shortcuts import reverse
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):    
    pass
```

#### Register custom user model into admin.py.

* Import UserAdmin from django contrib
* Import local User model
* Register the Model as a UserAdmin

```python
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
```

#### Add customer user model and login global variables to settings.py

``` python
LOGIN_URL = 'login'
LOGIN_REDIRECT_URL = 'index'

AUTH_USER_MODEL = 'users.User'
```


#### Create urls.py in user app.

```python
from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='index' ), name='logout'),
]

```

#### Forward account/ urls to user app in project urls.py

Add `path('accounts/', include('users.urls')),` as first entry in of `urlpatterns` array.



#### (REGISTRATION optional) Add custom user registration form

```python
from django.contrib.auth.forms import UserCreationForm

from .models import User

class CustomUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('username',)
```

#### (REGISTRATION optional) Create registration view

Add register view to `views.py`

```python
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import CustomUserCreationForm


def register(request):
    if request.method == 'POST':
        f = CustomUserCreationForm(request.POST)
        if f.is_valid():
            f.save()
            messages.success(request, 'Account created successfully')
            return redirect('register')
 
    else:
        f = CustomUserCreationForm()
 
    return render(request, 'registration/register.html', {'form': f}) 
```

#### Uncomment Login / Logout links in base.html template

#### Make migrations and migrate.

```bash
python manage.py makemigrations
python manage.my migrate
```

#### Create a superuser

```bash
python manage.py createsuperuser
```