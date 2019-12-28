from django.test import SimpleTestCase
import ast

class SimplerTestCase(SimpleTestCase):
    def assertTrue(self, expr, msg=None):
        if (not expr):
            self.fail(msg or (str(expr) + "is not True"))

    @staticmethod
    def load_ast_tree(filename):
        with open(filename) as f:
            fstr = f.read()
        return ast.parse(fstr, filename=filename)