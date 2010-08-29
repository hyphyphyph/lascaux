from libel import SObject


class SObject(SObject):
    __lib_import__ = __import__("lascaux")
