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
            self.str_method_found = False
            self.clean_method_found = False
            self.clean_assign_found = False
            self.tags_field_found = False
            self.tag_many_to_many_found = False

            self.check_model_file()


    def check_model_file(self):
        try:
            for x in self.load_ast_tree('mainapp/models.py').body:
                if isinstance(x, ast.ClassDef):
                    if x.name == 'Tag':
                        self.class_found = True
                        if (len(x.bases) > 0 and
                            x.bases[0].value.id == 'models' and
                            x.bases[0].attr == 'Model'):
                            self.base_class_found = True
                        for y in x.body:
                            if (isinstance(y, ast.Assign) and
                                    y.targets[0].id == 'name' and
                                    y.value.func.value.id == 'models' and
                                    y.value.func.attr == 'CharField'):
                                self.title_found = True
                                if (y.value.keywords[0].arg == 'max_length' and
                                        getattr(y.value.keywords[0].value, self.value_num) == 50):
                                    self.max_length_found = True

                            if (isinstance(y, ast.FunctionDef) and
                                    y.name == '__str__' and y.args.args[0].arg == 'self'):
                                for z in y.body:
                                    if (isinstance(z, ast.Return) and
                                        z.value.value.id == 'self' and
                                        z.value.attr == 'name'):
                                        self.str_method_found = True
                                        
                            if (isinstance(y, ast.FunctionDef) and
                                    y.name == 'clean' and y.args.args[0].arg == 'self'):
                                self.clean_method_found = True
                                for z in y.body:
                                    if (isinstance(z, ast.Assign) and
                                        z.targets[0].value.id == 'self' and
                                        z.targets[0].attr == 'name' and 
                                        z.value.func.value.value.id == 'self' and
                                        z.value.func.value.attr == 'name' and
                                        z.value.func.attr == 'lower'):
                                        self.clean_assign_found = True

                    elif x.name == 'BlogPost':
                        for y in x.body:
                            if (isinstance(y, ast.Assign) and
                                    y.targets[0].id == 'tags' and
                                    y.value.func.value.id == 'models' and
                                    y.value.func.attr == 'ManyToManyField'):
                                self.tags_field_found = True
                                if (len(y.value.keywords) > 0 and 
                                        y.value.keywords[0].arg == 'related_name' and
                                        getattr(y.value.keywords[0].value, self.value) == 'posts' and
                                        len(y.value.args) > 0 and
                                        getattr(y.value.args[0], self.value) == 'Tag'):
                                    self.tag_many_to_many_found = True
        except Exception as e:
            # printe)
            pass
            


    def test_task1_tag_model_exists(self):    
        """ Add Tag model to models.py
            class Tag(models.Model):
                name = models.CharField(max_length=50, unique=True) """
        
        self.assertTrue(self.class_found, msg="Did you create the `Tag` class?")
        self.assertTrue(self.base_class_found, msg="Make sure you added `models.Model` as the base class of `BlogPost`.")
        self.assertTrue(self.title_found, msg="Did you add the `name` field?")
        self.assertTrue(self.max_length_found, msg="Did you set `max_length` in the `CharField`?")

    def test_task2_clean_method_exists(self):
        """Add clean method to sanitize input."""
        self.assertTrue(self.clean_method_found, msg="Did you implement the `clean` method in the `tag` model class?")
        self.assertTrue(self.clean_assign_found, msg="Did you assign to `self.name` in the `clean` method?")

    def test_task3_str_exists(self):
        self.assertTrue(self.str_method_found, msg="Did you implement the `__str__` method in the `tag` model class?")

    def test_task4_many_to_many_exists(self):
        self.assertTrue(self.tags_field_found, msg="Did you add the `name` field?")
        self.assertTrue(self.tag_many_to_many_found, msg="Did you set `tags` equal to the `ManyToManyField`?")
