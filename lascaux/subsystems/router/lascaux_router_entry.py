import os.path
import glob

import lascaux
from lascaux.util import parse_config, SUPPORTED_CONFIG_EXTENSIONS
from lascaux import logger
logger = logger(__name__)

import instlatte


class RouterSubsystem(instlatte.SubSystem):

    def get_sources(self):
        sources = []
        obj = lascaux.Object()
        sources.append(os.path.join(obj.get_lib_path(), "routers"))
        sources.append(os.path.join(self.get_exec_path(), "routers"))
        return sources

    def discover_plugins(self):
        for source in self.get_sources():
            for config_path in glob.glob(os.path.join(source, "*", "*.json")):
                if os.path.splitext(config_path)[1] in \
                    SUPPORTED_CONFIG_EXTENSIONS:
                    config = parse_config(config_path)
                    config_ = {
                        "name": config["name"],
                        "config": config,
                        "config_filename": config_path,
                        "path": os.path.dirname(config_path)
                    }
                    logger.info("Found router: `%s` using %s" % \
                        (config["name"], config_path))

    def load_plugin(self, Plugin):
        pass
