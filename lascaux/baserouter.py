from lascaux.sys import SObject


class BaseRouter(SObject):

    def find_route(self, app, request):
        pass

    def exec_route(self, app, request):
        instance = request.exec_plugin["__class__"](request)
        method = getattr(instance, request.exec_route["action"])
        app.hook("pre_exec", {"app": app,
                              "request": request,
                              "controller": instance,
                              "method": request.exec_route["action"],
                              "args": request.exec_args})
        return_ = method(**request.exec_args)
        app.hook("post_exec", {"app": app,
                              "request": request,
                              "controller": instance,
                              "method": request.exec_route["action"],
                              "args": request.exec_args,
                              "return_": return_})
        if isinstance(return_, Redirect):
            request.flag_redirect = True
            request.URI = return_.where or "/"
            request.set_http_code(return_.code)
            request.headers["Location"] = request.URI
        elif isinstance(return_, basestring):
            request.set_content(return_, plain=True)
        return return_

    def get_route(self, controller, action, args={}):
        pass
