if __name__ == "__main__": import sys; sys.path.append(".")
import unittest

from petrified.mirror import Mirror


class MirrorForTest(Mirror):

    exists = True


class TestMirror(unittest.TestCase):

    def setUp(self):
        self.mirror = MirrorForTest()

    def test_accessible(self):
        self.mirror.name = True
        self.assertTrue(self.mirror.name)
        self.mirror.make_normal()
        a = False
        try:
           a = self.mirror.name and True
        except: pass
        self.assertFalse(a)
            


if __name__ == "__main__":
    unittest.main()
