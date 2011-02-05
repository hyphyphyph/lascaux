from storm.locals import *


class HelloWorldMessage(object):
    
    __storm_table__ = "hello_world"
    __export_to_model__ = True

    id = Int(primary=True)
    message = Unicode(default=u"Hello World")
