import os.path
import glob

from instlatte import Subsystem

import lascaux
from lascaux.sys import logger
from lascaux.session import SessionStore


logger = logger(__name__)


class SessStoreSubsystem(Subsystem):

    def get_sources(self):
        sources = set()
        map(sources.add, [os.path.join(os.path.dirname(app.__file__),
                                       'sess_stores')
                          for app in lascaux.app_packages])
        sources.add(os.path.join(lascaux.__lib_path__, 'sess_stores'))
        return list(sources)

    def discover_plugins(self):
        for source in self.get_sources():
            for s in filter(lambda f:
                            not os.path.basename(f).startswith('_'),
                            glob.glob(os.path.join(source, '*.py'))):
                name = os.path.basename(os.path.splitext(s)[0])
                p = self.new_plugin(name=name, package_dir=source,
                                    entry_module=name)
                logger.info(u"%s: discovered sess_store plugin '%s'" %
                            (self.meta.name, p.name))
                self.add_plugin(p)
        return True

    def task___load_enabled_plugins__(self):
        for plugin in self.meta.get_enabled_plugins_list():
            if self._load_plugin(plugin):
                logger.info("[+] loaded plugin '%s'" % plugin.name)
            else:
                logger.error("failed to load plugin '%s'" % plugin.name)

    def _load_plugin(self, plugin):
        dot_path = self.determine_dot_path(os.path.join(plugin.package_dir,
                                                        plugin.entry_module))
        module = __import__(dot_path)
        for fragment in dot_path.split('.')[1:]:
            module = getattr(module, fragment)
        for symbol in dir(module):
            symbol = getattr(module, symbol)
            if type(symbol) == type(SessionStore) and \
               SessionStore in symbol.__bases__:
                plugin.class_ = symbol
                plugin.instance = plugin.class_()
                return True
        return False

    def task_load(self, session):
        return_ = list()
        for plugin in self.meta.get_enabled_plugins_list():
            return_.append(plugin.instance.load(session))
        return return_

    def task_save(self, session):
        return_ = list()
        for plugin in self.meta.get_enabled_plugins_list():
            return_.append(plugin.instance.save(session))
        return return_
