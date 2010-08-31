import weakref
import mimetypes
import os.path

from lascaux import SObject


class BaseServer(SObject):

    app = None

    def init_server(self, App):
        self.app = weakref.proxy(App)

    def handle_request(self, Env):
        pass

    def handle_static_serve(self, Env, URI):
        pass
