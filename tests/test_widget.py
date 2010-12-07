if __name__ == "__main__": import sys; sys.path.append('.')
import unittest

from petrified.widget import Widget


class TestWidget(unittest.TestCase):

    def setUp(self):
        self.POST = dict(first_name=u'Derek',
                         last_name=u'Mounce')

    def test_init(self):
        widget = Widget()

    def test_ingest_POST(self):
        widget = Widget(name='first_name')
        widget.ingest_POST(self.POST)
        self.assertEqual(widget.value, u'Derek')

    def test_validate(self):
        widget = Widget(required=True, name='first_name')
        widget.validate()
        self.assertEqual(widget.value, u'')
        self.assertTrue(widget.error)
        

if __name__ == "__main__":
    unittest.main()
