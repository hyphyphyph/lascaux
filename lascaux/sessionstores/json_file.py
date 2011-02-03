# -*- coding: utf-8 -*-

import os.path

try:
    import json
except:
    import simplejson as json

import libel

from lascaux import config
from lascaux.sys.logger import logger
from lascaux.session import SessionStore


logger = logger(__name__)


class JsonFileSessionStore(SessionStore):

    def save(self, session):
        if not os.path.isdir(self.config['data_dir']):
            libel.mkdir(self.config['data_dir'])
        file = open(os.path.join(self.config['data_dir'],
                                 session.uuid), 'w+')
        file.write(json.dumps(session))
        file.close()

    def load(self, session):
        path = os.path.join(self.config['data_dir'], session.uuid)
        try:
            file = open(path)
            data = json.loads(file.read())
            file.close()
            for key in data:
                session[key] = data[key]
        except Exception, e:
            logger.error("Couldn't load session from json %s" % path)
