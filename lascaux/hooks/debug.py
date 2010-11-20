from lascaux.locals import Hook
from lascaux.sys import config


class DebugHook(Hook):

    def hook_request_close(self, request):
        if not config.get('debug'):
            pass
        request.debug('headers', unicode(request.get_http_headers()))
        request.debug('cookies', unicode(request.cookies))
        request.debug('session.uuid', unicode(request.session.uuid))
        request.debug('session', unicode(request.session))
