import os.path
import glob

import lascaux
from lascaux.sys import SObject, logger
from lascaux.baseserver import BaseServer

import instlatte


logger = logger(__name__)


class ServerSubsystem(instlatte.Subsystem):

    def discover_plugins(self):
        sources = [os.path.join(lascaux.__lib_path__, 'servers')]
        for source in sources:
            for s in filter(lambda f:
                            not os.path.basename(f).startswith('_'),
                            glob.glob(os.path.join(source, '*.py'))):
                name = os.path.basename(os.path.splitext(s)[0])
                p = self.new_plugin(name=name, package_dir=source,
                                    entry_module=name)
                logger.info(u"%s: discovered server plugin '%s'" %
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
            if type(symbol) == type(BaseServer) and \
               BaseServer in symbol.__bases__:
                plugin.class_ = symbol
                return True
        return False

    def task_start_server(self, app):
        server = self.meta.get_enabled_plugins_list()[0]
        instance = server.class_()
        instance.start(app)
