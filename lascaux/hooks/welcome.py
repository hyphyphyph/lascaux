from lascaux import Hook


class Welcome(Hook):

    def hook_app_init(self, app):
        print "Welcome to Lascaux!"
