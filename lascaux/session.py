# -*- coding: utf-8 -*-

import weakref
import uuid

from lascaux import config


class Session(dict):

    reqres = None
    uuid = None

    def __init__(self, reqres):
        self.reqres = weakref.proxy(reqres)

    def save(self):
        app = self.reqres.app
        session_subsystem = app.manager.get_subsystem('session')
        self.reqres.cookies[session_subsystem.config['cookie_uuid_key']] = self.uuid
        for store in session_subsystem.stores:
            store.save(self)

    def load(self):
        app = self.reqres.app
        session_subsystem = app.manager.get_subsystem('session')
        self.uuid = self.reqres.cookies.get(session_subsystem.config["cookie_uuid_key"])
        if not self.uuid:
            self.uuid = self._gen_sess_uuid()
        for store in session_subsystem.stores:
            store.load(self)

    def _gen_sess_uuid(self):
        # TODO: str or unicode ?
        return str(uuid.uuid1())


class SessionStore(object):

    config = dict()

    def __init__(self, config=dict()):
        self.config = config or dict()

    def load(self, session): pass
    def save(self, session): pass
