from storm.locals import *


class Setting(object):

    __export_to_model__ = True
    __storm_table__ = "setting"

    name = Unicode(primary=True)
    value = Unicode()
