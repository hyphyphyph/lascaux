from lascaux.sys import SObject
# from lascaux.config import config


class Redirect(SObject):

    where = None
    code = None

    def __init__(self, where, code=None):
        self.where = where
        self.code = code or config["defaults"]["redirect_code"]
