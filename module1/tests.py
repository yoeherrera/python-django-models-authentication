from django.test import SimpleTestCase
from django.conf import LazySettings
from django.conf import settings

import os

class UsersTestCase(SimpleTestCase):
    def test_task1_createapp(self):
        self.assertTrue(os.path.isdir('users'))
        self.assertTrue(os.path.isfile('users/admin.py'))
        self.assertTrue(os.path.isfile('users/apps.py'))
        self.assertTrue(os.path.isfile('users/models.py'))
        self.assertTrue(os.path.isfile('users/views.py'))


    def test_task2_add_settings(self):
        self.assertIn(settings.INSTALLED_APPS, 'users')

    def test_task3_add_template(self):
        self.assertTrue(os.path.isdir('users/templates'))
        self.assertTrue(os.path.isfile('users/templates/login.html'))