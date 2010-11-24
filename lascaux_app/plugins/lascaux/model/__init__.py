from storm.locals import *


class LascauxApp(object):

    __export_to_model__ = True
    __storm_table__ = "lascaux_app"

    id = Int(primary=True)
