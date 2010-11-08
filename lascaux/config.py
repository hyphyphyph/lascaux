import os.path
import glob
import hashlib

from libel import merge_dict

import lascaux
from lascaux.logger import logger
from lascaux.util import parse_config, SUPPORTED_CONFIG_EXTENSIONS
from lascaux.sys import SObject
from lascaux.lib import instlattesetup


logger = logger(__name__)


class Config(dict, SObject):
    def __init__(self):
        self.m = instlattesetup.new_plugin_manager()

    def reload(self):
        sources = set()
        map(sources.add, [p.package_dir for p in
                         self.m.get_enabled_subsystems_list()[0]. \
                         get_enabled_plugins_list()])
        map(sources.add, [os.path.dirname(p.__file__) for p in
                          lascaux.app_packages])
        sources.add(lascaux.__lib_path__)
        for source in sources:
            for c in glob.glob(os.path.join(source, 'config', '*.*')):
                if os.path.splitext(c)[1] in SUPPORTED_CONFIG_EXTENSIONS:
                    try:
                        config = parse_config(c)
                        merge_dict(self, config)
                        logger.debug(u"loaded config file %s" % c)
                    except Exception, e:
                        logger.error(u"failed to laod config file %s" % c)
        self._parse_special()

    def sap(self, String=""):
        """ Salt and pepper """
        return self["security"]["salt"]+u"%s"%String+self["security"]["pepper"]

    def _parse_special(self):
        self["paths"]["tmp"] = os.path.abspath(self["paths"]["tmp"])
        self["session"]["store_path"] = os.path.abspath(self["session"] \
                                                        ["store_path"])
        self["security"]["salt_raw"] = self["security"]["salt"]
        self["security"]["salt"] = hashlib.sha1(self["security"] \
                                                ["salt"]).hexdigest()
        self["security"]["pepper_raw"] = self["security"]["pepper"]
        self["security"]["pepper"] = hashlib.sha1(self["security"] \
                                                  ["pepper"]).hexdigest()

    def get_tmp(self):
        return self["paths"]["tmp"]

config = Config()
config.reload()
