import weakref
import uuid

from lascaux.sys import SObject, config


class Session(dict, SObject):

    request = None
    uuid = None

    def __init__(self, request):
        self.request = weakref.proxy(request)

    def save(self):
        app = self.request.app
        self.request.cookies.set(config["session"]["cookie_uuid_key"],
                                 self.uuid)
        return False not in \
               app.manager.execute('save', dict(session=self),
                                   subsystem='sess_store')

    def load(self):
        self.uuid = self.request.cookies.get(config["session"] \
                                             ["cookie_uuid_key"])
        if not self.uuid:
            self.uuid = self._gen_sess_uuid()
        app = self.request.app
        return False not in \
                app.manager.execute('load', dict(session=self),
                                    subsystem='sess_store')

    def _gen_sess_uuid(self):
        # TODO: str or unicode ?
        return str(uuid.uuid1())


class SessionStore(SObject):

    def load(self, session): pass
    def save(self, session): pass
