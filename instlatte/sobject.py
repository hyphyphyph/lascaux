import sys
import os
import os.path

from libel import SObject


class Object(SObject):

    __lib_import__ = __import__("instlatte")
