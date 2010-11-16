from lascaux.locals import Redirect
from lascaux.sys import SObject


class BaseRouter(SObject):

    def find_route(self, app, request):
        pass

    def exec_route(self, app, request):
        # Doing this just because maybe for whatever reason there might be possibly a potential instance. :)
        if request.exec_plugin.instance:
            instance = request.exec_plugin.instance
        else:
            instance = request.exec_plugin.class_(request)
        method = getattr(instance, request.exec_route["action"])
        app.hook("pre_exec", dict(request=request,
                                  controller=instance,
                                  action=request.exec_route["action"],
                                  args=request.exec_args))
        return_ = method(**request.exec_args)
        app.hook("post_exec", dict(request=request,
                                   controller=instance,
                                   action=request.exec_route["action"],
                                   args=request.exec_args,
                                   return_=return_))
        if isinstance(return_, Redirect):
            request.flag_redirect = True
            request.uri = return_.where or u"/"
            request.set_http_code(return_.code)
            request.headers["Location"] = request.uri
        elif isinstance(return_, basestring):
            request.set_content(return_, plain=True)
        return return_

    def get_route(self, controller, action, args={}):
        pass
