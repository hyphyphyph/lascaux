if __name__ == "__main__": import sys; sys.path.append('.')
import unittest
import os.path

from mako.template import Template

from petrified.form import Form
from petrified.widget import Widget


class TestForm(unittest.TestCase):

    def test_basic_render(self):
        form = Form()
        form.first_name = Widget()
        form.last_name = Widget()
        print form.render()

    # def test_complex_render(self):
    #     form = Form()
    #     form.first_name = Widget()
    #     form.last_name = Widget()
    #     form.render()

    # def test_partial_render(self):
    #     form = Form()
    #     form.widget_mode()
    #     form.first_name = Widget()
    #     form.last_name = Widget()
    #     t = Template(filename=os.path.abspath(
    #         os.path.join(os.path.dirname(__file__), 'form.mako')))
    #     print t.render(form=form)

        
if __name__ == "__main__":
    unittest.main()
