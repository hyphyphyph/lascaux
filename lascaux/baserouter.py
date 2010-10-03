from lascaux.model import create_store
from lascaux import SObject


class BaseRouter(SObject):
    def __init__(self):
        pass

    def find_route(self, App, Request):
        pass

    def exec_route(self, App, Request):
        instance = Request.exec_plugin["__class__"](Request)
        instance.db = create_store()
        method = getattr(instance, Request.exec_route["action"])
        return method(**Request.exec_args)
    
    def get_route(self, controller, action, args={}):
        pass