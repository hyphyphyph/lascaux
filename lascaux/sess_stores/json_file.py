try:
    import json
except:
    import simplejson as json
import os.path

import libel

from lascaux.sys import config, logger
from lascaux.session import SessionStore


logger = logger(__name__)


class JsonFileSessStore(SessionStore):

    def save(self, session):
        if not os.path.isdir(config["session"]["store_path"]):
            libel.mkdir(config["session"]["store_path"])
        file = open(os.path.join(config["session"]["store_path"],
                                 session.uuid), "w+")
        file.write(json.dumps(session))
        file.close()

    def load(self, session):
        path = os.path.join(config["session"]["store_path"], session.uuid)
        try:
            file = open(path)
            data = json.loads(file.read())
            file.close()
            for key in data:
                session[key] = data[key]
        except Exception, e:
            logger.error(u"couldn't load session from json %s" % path)
