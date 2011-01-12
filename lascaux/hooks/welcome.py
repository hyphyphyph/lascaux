from lascaux.locals import Hook


class Welcome(Hook):

    def hook_app_init(self):
        print "Welcome to Lascaux!"
