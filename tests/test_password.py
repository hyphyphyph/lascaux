if __name__ == "__main__": import sys; sys.path.append('.')
import unittest

from petrified.form import Form
from petrified.widgets import Password


class TestPassword(unittest.TestCase):

    def test_render(self):
        form = Form()
        form.password = Password()
        print form.password.render()


if __name__ == "__main__":
    unittest.main()
