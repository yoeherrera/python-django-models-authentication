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
        except:
            pass
    

    def test_task1_tag_model_exists(self):    
        """ Add Tag model to models.py
            class Tag(models.Model):
                name = models.CharField(max_length=50, unique=True)
        """
        
        self.assertTrue(self.class_found, msg="Did you create the `Tag` class?")
        self.assertTrue(self.base_class_found, msg="Make sure you added `models.Model` as the base class of `BlogPost`.")
        self.assertTrue(self.title_found, msg="Did you add the `name` field?")
        self.assertTrue(self.max_length_found, msg="Did you set `max_length` in the `CharField`?")


      