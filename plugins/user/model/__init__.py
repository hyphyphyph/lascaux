from storm.locals import *


class User(object):
    
    __export_to_model__ = True
    __storm_table__ = "user"
    
    uuid = Unicode(primary=True)
    username = Unicode()
    email = Unicode()
    password = Unicode()
    created = Int()
    lastlogin = Int()
    
    def __init__(self, uuid):
        self.uuid = uuid