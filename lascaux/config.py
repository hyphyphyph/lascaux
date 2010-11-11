import os.path
import glob
import hashlib

from libel import merge_dict

import lascaux
from lascaux.subsystems.plugin.lib import get_plugin_dirs, is_plugin_enabled
from lascaux.logger import logger
from lascaux.util import parse_config, SUPPORTED_CONFIG_EXTENSIONS


logger = logger(__name__)


class Config(dict):
    def __init__(self):
        self.refresh()

    def refresh(self):
        sources = list()
        map(sources.append, [os.path.abspath(os.path.dirname(p.__file__))
                             for p in lascaux.app_packages])
        map(sources.append, get_plugin_dirs())
        sources.append(lascaux.__lib_path__)
        merge_dict(lascaux.__config__, self)
        for source in sources:
            for c in glob.glob(os.path.join(source, 'config', '*.*')):
                if os.path.splitext(c)[1] in SUPPORTED_CONFIG_EXTENSIONS:
                    try:
                        config = parse_config(c)
                        merge_dict(self, config)
                        logger.debug(u"loaded config %s" % c)
                    except Exception, e:
                        logger.error(u"failed to laod config %s" % c)
        for c in glob.glob(os.path.join(lascaux.__exec_path__, 'config.*')):
            if os.path.splitext(c)[1] in SUPPORTED_CONFIG_EXTENSIONS:
                config = parse_config(c)
                merge_dict(self, config)
                logger.debug(u"loaded config %s" % c)
        self._parse_special()

    def sap(self, String=""):
        """Salt and pepper"""
        return self['security']['salt']+u'%s' % String + self['security']['pepper']

    def _parse_special(self):
        self['paths']['tmp'] = os.path.abspath(self['paths']['tmp'])
        self['session']['store_path'] = os.path.abspath(self['session'] \
                                                        ['store_path'])
        self['security']['salt_raw'] = self['security']['salt']
        self['security']['salt'] = hashlib.sha1(self['security'] \
                                                ['salt']).hexdigest()
        self['security']['pepper_raw'] = self['security']['pepper']
        self['security']['pepper'] = hashlib.sha1(self['security'] \
                                                  ['pepper']).hexdigest()

    def get_tmp(self):
        return self["paths"]["tmp"]

config = Config()
