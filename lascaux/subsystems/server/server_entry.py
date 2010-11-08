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
            for s in filter(lambda f:\
                            not os.path.basename(f).startswith('_'),
                            glob.glob(os.path.join(source, '*.py'))):
                name = os.path.basename(os.path.splitext(s)[0])
                p = self.new_plugin(name=name, package_dir=source,
                                    entry_module=name)
                logger.info(u"%s: discovered server plugin '%s'" % (self.meta.name, p.name))
                self.add_plugin(p)
        return True
