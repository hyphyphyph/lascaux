import os.path
import glob

from lascaux import SObject
from lascaux import logger
logger = logger(__name__)

import instlatte

from lascaux.baseserver import BaseServer


class ServerSubsystem(instlatte.SubSystem):

    def _discover_plugins(self):
        obj = SObject()
        for source in self.config["sources"]+ \
            [os.path.join(obj.get_lib_path(), "servers")]:
            for file in filter(lambda f: \
                not os.path.basename(f).startswith("_") \
                and not os.path.basename(f).startswith("."),
                               glob.glob(os.path.join(source, "*.py"))):
                self.plugins.append({
                    "name": os.path.basename(os.path.splitext(file)[0]),
                    "__file__": file
                })

    def _load_plugin(self, Plugin):
        module = self.import_file(Plugin["__file__"])
        for symbol in dir(module):
            symbol = getattr(module, symbol)
            if type(symbol) == type(self.__class__):
                if issubclass(symbol, BaseServer) and \
                   BaseServer in symbol.__bases__:
                    Plugin["__instance__"] = symbol()

    def execute(self, Plugin, Command, Data={}):
        if Command == "init_server":
            Plugin["__instance__"].init_server(Data["app"])
