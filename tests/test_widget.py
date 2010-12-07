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

    def test_render(self):
        widget = Widget(name='first_name')
        self.assertEqual(widget.render(),
                         '<input type="hidden" name="first_name" />')
        self.assertEqual(unicode(widget),
                         '<input type="hidden" name="first_name" />')
        

if __name__ == "__main__":
    unittest.main()
