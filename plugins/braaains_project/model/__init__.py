from storm.locals import *


class Project(object):

    __export_to_model__ = True
    __storm_table__ = "project"

    id = Int(primary=True)
    title = Unicode()
    desc = Unicode()
    enabled = Bool(default=True)
