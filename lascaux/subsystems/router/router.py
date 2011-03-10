import os.path
import glob

import instlatte
from instlatte.lib import Sentient

import lascaux
from lascaux.system.logger import logger
from lascaux.router import Router


logger = logger(__name__)


class RouterSubsystem(instlatte.Subsystem, Sentient):

    routers = list()

    def setup(self):
        self.config.setdefault('sources', list())
        self.config.setdefault('routers', dict())
        default_source = os.path.abspath(os.path.join(os.path.dirname(lascaux.__file__), 'routers'))
        if default_source not in self.config['sources']:
            self.config['sources'].insert(0, default_source)
        self.routers = list()

    def get_routers(self):
        return self.routers

    def exec_load_routers(self, app=None):
        self.load_routers(self.find_routers(), app)
    exec_app_init = exec_load_routers

    def find_routers(self):
        routers = dict()
        for source in self.config['sources']:
            for router in filter(lambda x: not os.path.basename(x).startswith('_')
                                           and not os.path.isdir(x),
                                 glob.glob(os.path.join(source, '*%spy' % os.path.extsep))):
                router_name = os.path.basename(os.path.splitext(router)[0])
                routers[router_name] = router
        return routers

    def load_routers(self, routers, app=None):
        for router in routers:
            router_name = router
            router = routers[router_name]
            if router_name not in self.config['routers'] \
               or not self.config['routers'][router_name]['enabled']:
                continue
            self._load_router(router, app)

    def _load_router(self, router, app=None):
        dotpath = self.get_dotpath(router)
        module = __import__(dotpath)
        for sym in dotpath.split('.')[1:]:
            module = getattr(module, sym)
        for sym in dir(module):
            sym = getattr(module, sym)
            if type(sym) == type(object) and Router in sym.__bases__:
                self.routers.append(sym(app=app))
