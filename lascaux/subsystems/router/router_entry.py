import os.path
import glob

import lascaux
from lascaux.sys import logger
from lascaux.baserouter import BaseRouter
import instlatte


logger = logger(__name__)


class RouterSubsystem(instlatte.Subsystem):

    def _get_sources(self):
        sources = set()
        sources.add(os.path.join(lascaux.__lib_path__, 'routers'))
        map(sources.add, [os.path.join(os.path.dirname(p.__file__), 'routers')
                          for p in lascaux.app_packages])
        return list(sources)

    def discover_plugins(self):
        for source in self._get_sources():
            for module in [r for r in glob.glob(os.path.join(source,
                                                             '*.py'))
                           if not os.path.basename(r).startswith('_')]:
                name = os.path.basename(os.path.splitext(module)[0])
                p = self.new_plugin(name=name,
                                    package_dir=os.path.dirname(module),
                                    entry_module=name)
                self.add_plugin(p)
        return True

    def task___load_enabled_plugins__(self):
        for plugin in self.meta.get_enabled_plugins_list():
            self._load_plugin(plugin)
            logger.info("loaded plugin '%s'" % plugin.name)

    def _load_plugin(self, plugin):
        dot_path = self.determine_dot_path(os.path.join(plugin.package_dir,
                                                        plugin.entry_module))
        module = __import__(dot_path)
        for fragment in dot_path.split('.')[1:]:
            module = getattr(module, fragment)
        for symbol in dir(module):
            symbol = getattr(module, symbol)
            if type(symbol) == type(BaseRouter) and \
               BaseRouter in symbol.__bases__:
                plugin.class_ = symbol
                return True
        return False
