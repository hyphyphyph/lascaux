import os.path
import glob

from lascaux import SObject
from lascaux import logger
logger = logger(__name__)

import instlatte

from lascaux.session import SessionStore


class SessStoreSubsystem(instlatte.SubSystem):

    def _discover_plugins(self):
        obj = SObject()
        for source in self.config["sources"]+ \
            [os.path.join(obj.get_lib_path(), "sess_stores")]:
            source = os.path.abspath(source)
            for file in filter(lambda f: \
                not os.path.basename(f).startswith("_") \
                and not os.path.basename(f).startswith("."),
                               glob.glob(os.path.join(source, "*.py"))):
                plugin = {
                    "name": os.path.basename(os.path.splitext(file)[0]),
                    "__file__": file }
                logger.info("Found session store %s" % plugin["name"])
                self.plugins.append(plugin)

    def _load_plugin(self, Plugin):
        module = self.import_file(Plugin["__file__"])
        for symbol in dir(module):
            symbol = getattr(module, symbol)
            if type(symbol) == type(self.__class__):
                if issubclass(symbol, SessionStore) and \
                   SessionStore in symbol.__bases__:
                    Plugin["__instance__"] = symbol()
                    logger.info("Loaded session store %s" % Plugin["name"])

    def execute(self, Plugin, Command, Data={}):
        if Command == "save":
            Plugin["__instance__"].save(**Data)
        elif Command == "load":
            Plugin["__instance__"].load(**Data)
