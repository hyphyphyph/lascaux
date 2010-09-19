import os.path
import glob

import lascaux
from lascaux.util import parse_config, SUPPORTED_CONFIG_EXTENSIONS
from lascaux.baserouter import BaseRouter
from lascaux import logger
logger = logger(__name__)

import instlatte


class RouterSubsystem(instlatte.SubSystem):

    def get_sources(self):
        sources = []
        obj = lascaux.SObject()
        sources.append(os.path.join(obj.get_lib_path(), "routers"))
        sources.append(os.path.join(self.get_exec_path(), "routers"))
        return sources

    def _discover_plugins(self):
        for source in self.get_sources():
            for config_path in glob.glob(os.path.join(source, "*", "*.json")):
                if os.path.splitext(config_path)[1] in \
                    SUPPORTED_CONFIG_EXTENSIONS:
                    config = parse_config(config_path)
                    config_ = {
                        "name": config["name"],
                        "__config__": config,
                        "__config_file__": config_path,
                        "__path__": os.path.dirname(config_path),
                    }
                    config_["__file__"] = os.path.join(config_["__path__"],
                                                       config_["name"])
                    self.plugins.append(config_)
                    logger.info("Found router: `%s` using %s" % \
                        (config_["name"], config_path))

    def _load_plugin(self, Plugin):
        print "--------------------------------------------------"
        module = self.import_file(Plugin["__file__"])
        for symbol in dir(module):
            symbol = getattr(module, symbol)
            if type(symbol) == type(self.__class__):
                if issubclass(symbol, BaseRouter) and \
                   BaseRouter in symbol.__bases__:
                    Plugin["__instance__"] = symbol()

    def execute(self, Plugin, Command, Data={}):
        if Command == "find_route":
            print Plugin
            # Plugin["__instance__"].init_server(Data["app"])
        return False
