import uuid
import weakref

from libel import cipher, sl

from lascaux import SObject, config


class Session(dict, SObject):

    request = None
    uuid = None

    def __init__(self, Request):
        self.request = weakref.proxy(Request)

    def save(self):
        app = self.request.app
        # Put the session's uuid into the cookie
        self.request.cookies.set(config["session"]["cookie_uuid_key"],
                                 self.uuid)
        return False not in app.manager.execute(app.manager. \
                select("subsystem", sl.EQUALS("lascaux_sess_store")). \
                select("name", sl.EQUALS(config["session"]["storage"])),
            "save", {"Session": self}).values()

    def load(self):
        if not self.request.cookies.get(config["session"] \
                                        ["cookie_uuid_key"]):
            self.uuid = self._gen_sess_uuid()
        else:
            self.uuid = self.request.cookies.get(config["session"] \
                                                 ["cookie_uuid_key"])
        app = self.request.app
        return False not in app.manager.execute(app.manager. \
                select("subsystem", sl.EQUALS("lascaux_sess_store")). \
                select("name", sl.EQUALS(config["session"]["storage"])),
            "load", {"Session": self}).values()

    def _gen_sess_uuid(self):
        return str(uuid.uuid1())

    def set(self, Key, Value):
        self[Value] = Value


class SessionStore(SObject):

    def load(self, Session):
        pass

    def save(self, Session):
        pass
