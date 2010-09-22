if __name__ == "__main__":
    import sys
    sys.path.append(".")

import os.path
import glob

from libel import merge_dict

from lascaux import logger
logger = logger(__name__)
from lascaux.util import parse_config, SUPPORTED_CONFIG_EXTENSIONS
from lascaux import SObject


class Config(dict, SObject):
    def reload(self):
        for source in (self.get_lib_path(), self.get_exec_path()):
            for config_file in glob.glob(os.path.join(source,
                                                      "config", "*.*")):
                if os.path.basename(config_file).startswith("_") or \
                   os.path.basename(config_file).startswith("."):
                    continue
                if os.path.splitext(config_file)[1] in \
                   SUPPORTED_CONFIG_EXTENSIONS:
                    try:
                        config = parse_config(config_file)
                        merge_dict(self, config)
                        logger.debug("Loaded and merged config file %s" %
                            config_file)
                    except Exception as e:
                        logger.error("Failed to load config file %s: %s" %
                            (config_file, e))
        self._parse_special()

    def _parse_special(self):
        self["paths"]["tmp"] = os.path.abspath(self["paths"]["tmp"])


config = Config()
config.reload()
