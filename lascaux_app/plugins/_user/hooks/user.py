from lascaux.model import User

from lascaux import Hook


class LoadUser(Hook):

    def hook_pre_exec(self, app, request, controller, method, args):
        if "user_uuid" in request.session:
            user = controller.db.get(User, request.session["user_uuid"])
            if user:
                if user.check_login(request):
                    controller.user = user
                    return
        controller.user = None
