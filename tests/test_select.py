if __name__ == "__main__": import sys; sys.path.append('.')
import unittest

from petrified.form import Form
from petrified.widgets import Select


class TestSelect(unittest.TestCase):

    def test_render(self):
        form = Form()
        form.select = Select(options=[
            ['value', 'text']
        ])
        print form.select.render()


if __name__ == "__main__":
    unittest.main()
