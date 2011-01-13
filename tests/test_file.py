if __name__ == "__main__": import sys; sys.path.append('.')
import unittest

from petrified.form import Form
from petrified.widgets import File


class TestFile(unittest.TestCase):

    def test_render(self):
        form = Form()
        form.file = File()
        print form.file.render()
        print form.render()


if __name__ == "__main__":
    unittest.main()
