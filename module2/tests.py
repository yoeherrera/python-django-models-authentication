import ast
from support.SimplerTestCase import SimplerTestCase

class PostTestCase(SimplerTestCase):
    setup_run = False
    def setUp(self):
        if not self.setup_run:
            self.setup_run = True 
            self.class_found = False
            self.base_class_found = False
            self.title_found = False
            self.max_length_found = False
            self.settings_import_found = False
            self.author_field_found = False
            self.author_user_model_found = False
            self.author_on_delete_found = False
            self.author_related_name_found = False
            self.body_field_found = False

            self.check_model_file()

    def check_model_file(self):
        try:
            for x in self.load_ast_tree('mainapp/models.py').body:
                if isinstance(x, ast.ImportFrom):
                    if x.module == 'django.conf' and x.names[0].name == 'settings':
                        self.settings_import_found = True

                if isinstance(x, ast.ClassDef):
                    if x.name == 'BlogPost':
                        self.class_found = True
                        if (len(x.bases) > 0 and
                            x.bases[0].value.id == 'models' and
                            x.bases[0].attr == 'Model'):
                            self.base_class_found = True
                        for y in x.body:
                            if (isinstance(y, ast.Assign) and
                                    y.targets[0].id == 'title' and
                                    y.value.func.value.id == 'models' and
                                    y.value.func.attr == 'CharField'):
                                self.title_found = True
                                if (y.value.keywords[0].arg == 'max_length' and
                                        y.value.keywords[0].value.value == 200):
                                    self.max_length_found = True
                            if (isinstance(y, ast.Assign) and
                                    y.targets[0].id == 'author' and
                                    y.value.func.value.id == 'models' and 
                                    y.value.func.attr == 'ForeignKey'):
                                self.author_field_found = True
                                if (y.value.args[0].value.id == 'settings' and
                                    y.value.args[0].attr == 'AUTH_USER_MODEL'):
                                    self.author_user_model_found = True
                                for keyword in y.value.keywords:
                                    if (keyword.arg == 'related_name' and 
                                        keyword.value.value == 'posts'):
                                        self.author_related_name_found = True
                                    if (keyword.arg == 'on_delete' and 
                                        keyword.value.value.id == 'models' and 
                                        keyword.value.attr == 'CASCADE'):
                                        self.author_on_delete_found = True
                                    if (keyword.arg == 'model' and
                                        keyword.value.value.id == 'settings' and 
                                        keyword.value.attr == 'AUTH_USER_MODEL'):
                                        self.author_user_model_found = True
                            if (isinstance(y, ast.Assign) and
                                    y.targets[0].id == 'body' and
                                    y.value.func.value.id == 'models' and
                                    y.value.func.attr == 'TextField'):
                                self.body_field_found = True

        except:
            pass


    def test_task1_post_model_exists(self):    
        """class BlogPost(models.Model):
            title = models.CharField(max_length=200)"""
        
        self.assertTrue(self.class_found, msg="Did you create the `BlogPost` class?")
        self.assertTrue(self.base_class_found, msg="Make sure you added `models.Model` as the base class of `BlogPost`.")
        self.assertTrue(self.title_found, msg="Did you add the `title` field?")
        self.assertTrue(self.max_length_found, msg="Did you set `max_length` in the `CharField`?")
        
    def test_task2_author_exists(self):
        """author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name="posts",
        on_delete=models.CASCADE,
        )"""
        
        self.assertTrue(self.settings_import_found, msg="Did you import `django.conf`'s `settings`")
        self.assertTrue(self.author_field_found, msg="Did you add the author field?")
        self.assertTrue(self.author_user_model_found, msg="Did you pass `AUTH_USER_MODEL` to `ForeignKey`?")
        self.assertTrue(self.author_related_name_found, msg="Did you set the `related_name` field in `ForeignKey`?")
        self.assertTrue(self.author_on_delete_found, msg="Did you set the `on_delete` field in `ForeignKey`?")

    def test_task3_body_exists(self):
        """ Add another field to `BlogPost` called `body` with type
        `models.TextField()`"""

        self.assertTrue(self.body_field_found, msg="Did you add the `body` field?")

    def test_task4_postdate_exists(self):
        """`postdate = models.DateTimeField(auto_now_add=True, blank=True)`"""
        self.assertTrue(self.postdate_field_found, msg="Did you add the `postdate` field and parameters?")
