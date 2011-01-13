if __name__ == "__main__": import sys; sys.path.append('.')
import unittest

from petrified.form import Form
from petrified.widgets import Button


class TestButton(unittest.TestCase):

    def test_render(self):
        form = Form()
        form.button = Button()
        print form.button.render()


if __name__ == "__main__":
    unittest.main()
