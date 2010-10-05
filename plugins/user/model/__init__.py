from storm.locals import *

from lascaux import config


class User(object):

    __export_to_model__ = True
    __storm_table__ = "user"

    uuid = Unicode(primary=True)
    username = Unicode()
    email = Unicode()
    password = Unicode()
    created = Int()
    lastlogin = Int()
    active = Bool(default=False)

    def __init__(self, uuid):
        self.uuid = uuid

    def login(self, request):
        if self.uuid:
            request.session["user_uuid"] = self.uuid
            request.session["user_username"] = config.sap(self.username)
            request.session["user_password"] = config.sap(self.password)
            return True
        return False

    def logout(self, request):
        request.session["user_uuid"] = None
        request.session["user_username"] = None
        request.session["user_password"] = None

    def check_login(self, request):
        r = request
        s = config.sap
        validity = [
            ("user_uuid" in r.session and
             r.session["user_uuid"] == self.uuid) or False,
            ("user_username" in r.session and
             r.session["user_username"] == s(self.username)) or False,
            ("user_password" in r.session and
             r.session["user_password"] == s(self.password)) or False]
        if False in validity:
            self.logout(request)
            return False
        return True
