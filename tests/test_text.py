if __name__ == "__main__": import sys; sys.path.append('.')
import unittest

from petrified.form import Form
from petrified.widgets import Text


class TestText(unittest.TestCase):

    def test_render(self):
        form = Form()
        form.text = Text()
        print form.text.render()
        form.text = Text(cols="42")
        print form.text.render()
        form.text = Text(cols="42", rows="21")
        print form.text.render()


if __name__ == "__main__":
    unittest.main()
