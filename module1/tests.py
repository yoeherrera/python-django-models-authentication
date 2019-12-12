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

