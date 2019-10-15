from django.test import SimpleTestCase
from mainapp import models as mainapp_models

from django.db.models.base import ModelBase
from django.conf import LazySettings
from django.db.models.fields.related_descriptors import ForwardManyToOneDescriptor
from django.db.models.deletion import CASCADE
from django.db.models.fields import CharField, DateTimeField, TextField
import users
import sys

class PostTestCast(SimpleTestCase):
    def test_settings_import(self):
        modulename = 'django.conf'
        self.assertTrue(modulename in sys.modules)
        self.assertTrue(type(mainapp_models.settings) == LazySettings)

    def test_post_model_exists(self):
        self.assertTrue( 'BlogPost' in dir(mainapp_models) and
                        type(mainapp_models.BlogPost) == ModelBase)

    def test_post_author_field(self):
        self.assertTrue( 'author' in dir(mainapp_models.BlogPost) and
                        type(mainapp_models.BlogPost.author) == ForwardManyToOneDescriptor)
        self.assertEqual(mainapp_models.BlogPost.author.field.related_query_name(),
                        'posts')
        # Note I should really be checking if its set to
        # settings.AUTH_USER_MODEL, not its value
        self.assertTrue(mainapp_models.BlogPost._meta.get_field('author').related_model == users.models.User)
        test_post = mainapp_models.BlogPost()
        self.assertEqual( test_post._meta.get_field('author').remote_field.on_delete,
                         CASCADE)

    def test_post_title_field(self):
        self.assertTrue('title' in dir(mainapp_models.BlogPost))
        self.assertEqual(type(mainapp_models.BlogPost._meta.get_field('title')),
                         CharField)
        self.assertEqual(mainapp_models.BlogPost._meta.get_field('title').max_length,
                         200)

    def test_post_body_field(self):
        self.assertTrue('body' in dir(mainapp_models.BlogPost))
        self.assertEqual(type(mainapp_models.BlogPost._meta.get_field('body')),
                         TextField)
 
    def test_post_postdate_field(self):
        self.assertTrue('postdate' in dir(mainapp_models.BlogPost))
        self.assertEqual(type(mainapp_models.BlogPost._meta.get_field('postdate')),
                         DateTimeField)
        # Add autoadd now and blnak checks 


