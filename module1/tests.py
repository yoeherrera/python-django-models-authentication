from django.test import SimpleTestCase
from django.conf import LazySettings
from django.conf import settings

import os, ast

def load_ast_tree(filename):
    with open(filename) as f:
        fstr = f.read()
    return ast.parse(fstr, filename=filename)

class UsersTestCase(SimpleTestCase):
    def test_task1_createapp(self):
        self.assertTrue(os.path.isdir('users'), msg="Did you use `manage.py createapp` to start the `users` app?")
        self.assertTrue(os.path.isfile('users/admin.py'), msg="Did you use `manage.py createapp` to start the `users` app?")
        self.assertTrue(os.path.isfile('users/apps.py'), msg="Did you use `manage.py createapp` to start the `users` app?")
        self.assertTrue(os.path.isfile('users/models.py'), msg="Did you use `manage.py createapp` to start the `users` app?")
        self.assertTrue(os.path.isfile('users/views.py'), msg="Did you use `manage.py createapp` to start the `users` app?")

    def test_task2_add_settings(self):
        self.assertIn('users', settings.INSTALLED_APPS, msg="Check if users app is in INSTALLED_APPS")

    def test_task3_add_template(self):
        self.assertTrue(os.path.isdir('users/templates'), msg="Did you create the `templates` directory in `users`?")
        self.assertTrue(os.path.isfile('users/templates/login.html'), msg="Did you copy the `login.html` file from the `support` folder?")

    def test_task4_create_model(self):
        import_found = False
        user_class_found = False
        user_base_class_found = False
        for x in load_ast_tree('users/models.py').body:
            if type(x) is ast.ImportFrom:
                if x.module == 'django.contrib.auth.models' and x.names[0].name == 'AbstractUser':
                    import_found = True
            if type(x) is ast.ClassDef:
                if x.name == 'User':
                    user_class_found = True
                if len(x.bases) and x.bases[0].id == 'AbstractUser':
                    user_base_class_found = True

        self.assertTrue(import_found, msg="Did you import `AbstractUser`?")
        self.assertTrue(user_class_found, "Did you create the `User` class?")
        self.assertTrue(user_base_class_found, "Did you derive the `User` class from `AbstractUser`?")

    def test_task5_register_admin(self):
        """
In order to have access to this model in the admin, we need to register it in `admin.py`.  Let’s do the following:
`from django.contrib.auth.admin import UserAdmin`
`from .models import User`
Call `admin.site.register()` with `User` and `UserAdmin` as parameters."""

        import_user_admin_found = False
        import_user_model_found = False
        admin_site_register_found = False

        try:
            for x in load_ast_tree('users/admin.py').body:
                if type(x) is ast.ImportFrom:
                    if x.module == 'django.contrib.auth.admin' and x.names[0].name == 'UserAdmin':
                        import_user_admin_found = True
                    elif x.module == 'models' and x.names[0].name == 'User':
                        import_user_model_found = True
                elif type(x) is ast.Expr:   
                    if (x.value.func.value.value.id == 'admin' and 
                        x.value.func.value.attr == 'site' and
                        x.value.func.attr == 'register'):
                        if (x.value.args[0].id == 'User' and
                            x.value.args[1].id == 'UserAdmin'):
                            admin_site_register_found = True
        except:
            # Catch any bad things that happened above and fail the test.
            pass
        
        self.assertTrue(import_user_admin_found, msg="Did you import `UserAdmin`?")
        self.assertTrue(import_user_model_found, msg="Did you import the `User` model?")
        self.assertTrue(admin_site_register_found, msg="Did you remember to register the model to the admin site?")

    def test_task6_add_settings(self):
        self.assertEqual(settings.LOGIN_URL, 'login', msg="Check if you set `LOGIN_URL` in `settings.py`.")
        self.assertEqual(settings.LOGIN_REDIRECT_URL, 'index', msg="Check if you set `LOGIN_REDIRECT_URL` in `settings.py`.")
        self.assertEqual(settings.AUTH_USER_MODEL, 'users.User', msg="Check if you set `AUTH_USER_MODEL` in `settings.py`.")

    def test_task7_setup_urls(self):
        try:
            urls_ast = load_ast_tree('users/urls.py').body
        except FileNotFoundError:
            self.fail("Did you create the `urls.py` file?")

        auth_views_import_found = False
        path_import_found = False
        views_import_found = False
        login_path_found = False
        logout_path_found = False

        try:
            for x in urls_ast:
                if type(x) is ast.ImportFrom:
                    if (x.module == 'django.contrib.auth' and 
                        x.names[0].name == 'views' and 
                        x.names[0].asname == 'auth_views'):
                        auth_views_import_found = True
                    elif x.module == None and x.names[0].name == 'views':
                        views_import_found = True
                    elif x.module == 'django.urls' and x.names[0].name == 'path':
                        path_import_found = True
                elif type(x) is ast.Assign and x.targets[0].id == 'urlpatterns':                    
                    login_path_found, logout_path_found =  self.check_urlpatterns(x)
        except:
            # Catch any bad things that happened above and fail the test.
            pass

        self.assertTrue(auth_views_import_found, 'Did you import `auth_views`?')
        self.assertTrue(path_import_found, 'Did you import `path` from `django.urls`?')
        self.assertTrue(views_import_found, 'Did you import the local `views`?')
        self.assertTrue(login_path_found, "Did you add the `urlpatterns` array?")
        self.assertTrue(logout_path_found, "Did you add the `urlpatterns` array?")
    
    def check_urlpatterns(self, node):
        login_path_found = False
        logout_path_found = False

        routes = node.value.elts
        for entry in routes:
            if (entry.func.id == 'path' and 
                entry.args[0].value == 'login/' and 
                entry.args[1].func.value.value.id == 'auth_views' and 
                entry.args[1].func.value.attr == 'LoginView' and 
                entry.args[1].func.attr == 'as_view' and 
                entry.args[1].keywords[0].arg == 'template_name' and 
                entry.args[1].keywords[0].value.value == 'login.html' and 
                entry.keywords[0].arg == 'name' and 
                entry.keywords[0].value.value == 'login' ):
                """path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),"""
                login_path_found = True
            elif (entry.func.id == 'path' and 
                entry.args[0].value == 'logout/' and 
                entry.args[1].func.value.value.id == 'auth_views' and 
                entry.args[1].func.value.attr == 'LogoutView' and 
                entry.args[1].func.attr == 'as_view' and 
                entry.args[1].keywords[0].arg == 'next_page' and 
                entry.args[1].keywords[0].value.value == 'index' and 
                entry.keywords[0].arg == 'name' and 
                entry.keywords[0].value.value == 'logout' ):
                """    path('logout/', auth_views.LogoutView.as_view(next_page='index' ), name='logout'),"""
                logout_path_found = True
        return login_path_found, logout_path_found
