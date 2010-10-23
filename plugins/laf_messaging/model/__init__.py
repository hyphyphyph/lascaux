from storm.locals import *


class LafMessage(object):

    __export_to_model__ = True
    __storm_table__ = "message"

    id = Int(primary=True)
    subject = Unicode()
    body = Unicode()
    date = Int()
    read = Bool()
    uuid_sender = Unicode()
    uuid_recipient = Int()
    parent_id = Int()
    item_id = Int()


def setup():
    from lascaux.model_setup import User, LafItem

    LafMessage.sender = Reference(LafMessage.uuid_sender, User.uuid)
    LafMessage.recipient = Reference(LafMessage.uuid_recipient, User.uuid)
    LafMessage.parent = Reference(LafMessage.parent_id, LafMessage.id)
    LafMessage.item = Reference(LafMessage.item_id, LafItem.id)
