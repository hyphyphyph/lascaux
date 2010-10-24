try:
    import json
except:
    import simplejson as json
import os.path

import libel

from lascaux import config

from lascaux.session import SessionStore


class JsonFileSessStore(SessionStore):

    def save(self, Session):
        if not os.path.isdir(config["session"]["store_path"]):
            libel.mkdir(config["session"]["store_path"])
        file = open(os.path.join(config["session"]["store_path"],
                                 Session.uuid), "w+")
        file.write(json.dumps(Session))
        file.close()

    def load(self, Session):
        try:
            file = open(os.path.join(config["session"]["store_path"],
                                     Session.uuid), "r")
            data = json.loads(file.read())
            file.close()
            for key in data:
                Session[key] = data[key]
        except:
            pass
