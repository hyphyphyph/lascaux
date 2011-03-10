import os.path
import glob

import instlatte
from instlatte.lib import Sentient

import lascaux
from lascaux import config
from lascaux.system.logger import logger
from lascaux.session import Session, SessionStore


logger = logger(__name__)


class SessionSubsystem(instlatte.Subsystem, Sentient):

    stores = list()

    def setup(self):
        self.config.setdefault('sources', list())
        default_source = os.path.abspath(os.path.join(os.path.dirname(lascaux.__file__), 'sessionstores'))
        if default_source not in self.config['sources']:
            self.config['sources'].insert(0, default_source)
        self.stores = list()

    def exec_load_sessionstores(self, app=None):
        self.find_and_load_sessionstores(app)
    exec_app_init = exec_load_sessionstores

    def find_and_load_sessionstores(self, app=None):
        for source in self.config['sources']:
            for sessionstore in filter(lambda f: not os.path.basename(f).startswith('_'),
                                           glob.glob(os.path.join(source, '*%spy' % os.path.extsep))):
                if os.path.isdir(sessionstore):
                    continue
                sessionstore_name = os.path.basename(os.path.splitext(sessionstore)[0])
                self._load_sessionstore(sessionstore, app)

    def _load_sessionstore(self, sessionstore, app=None):
        sessionstore_name = os.path.basename(os.path.splitext(sessionstore)[0])
        dotpath = self.get_dotpath(sessionstore)
        module = __import__(dotpath)
        for sym in dotpath.split('.')[1:]:
            module = getattr(module, sym)
        for sym in dir(module):
            sym = getattr(module, sym)
            if type(sym) == type(object) and SessionStore in sym.__bases__:
                self.stores.append(sym(config=self.config['stores'][sessionstore_name]))
