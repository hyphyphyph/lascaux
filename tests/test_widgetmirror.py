if __name__ == "__main__": import sys; sys.path.append(".")
import unittest

from petrified.widgetmirror import WidgetMirror


class WidgetMirrorForTest(WidgetMirror):

    exists = True


class DummyWidget(object):

    name = None

    def __init__(self, name):
        self.name = name

    def _get_title(self):
        return '%s <%s>' % (self.__class__.__name__, id(self))
    title = property(_get_title)


class TestWidgetMirror(unittest.TestCase):

    def setUp(self):
        self.mirror = WidgetMirrorForTest()


    def test_access(self):
        try:
            self.mirror.exists
        except:
            raise AttributeError("Couldn't access 'exists'")

    def test_AttributeError(self):
        try:
            self.mirror.doesntexise
            self.assertTrue(False)
        except:
            self.assertTrue(True)

    def test_modes(self):
        self.assertTrue(self.mirror.widget_mode())
        self.assertTrue(self.mirror.is_widget_mode)
        self.assertFalse(self.mirror.is_normal_mode)

        self.assertTrue(self.mirror.normal_mode())
        self.assertTrue(self.mirror.is_normal_mode)
        self.assertFalse(self.mirror.is_widget_mode)

    def test_append_widget(self):
        for x in xrange(5):
            self.mirror.append_widget(DummyWidget('dummy%s' % x))

    def test_widget_mode_access(self):
        for x in xrange(5):
            self.mirror.append_widget(DummyWidget('dummy%s' % x))
        self.mirror.widget_mode()
        self.assertEqual(self.mirror.dummy0.title.split(' ')[0], 'DummyWidget')
        self.mirror.normal_mode
        try:
            self.mirror.dummy0
        except:
            self.assertTrue(True)

    def test_widget_mode_set(self):
        self.mirror.name = '123'
        self.mirror.widget_mode()
        self.assertEqual(self.mirror.name, '123')
        self.mirror.dummy0 = DummyWidget('dummy0')
        self.assertEqual(self.mirror.dummy0.title.split(' ')[0], 'DummyWidget')
        self.mirror.normal_mode()
        try:
            self.mirror.dummy0
        except:
            self.assertTrue(True)
        self.assertEqual(self.mirror.name, '123')

if __name__ == "__main__":
    unittest.main()
