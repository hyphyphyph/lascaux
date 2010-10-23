from storm.locals import *


class LafItem(object):

    __export_to_model__ = True
    __storm_table__ = "item"

    id = Int(primary=True)
    title = Unicode()
    kind = Unicode()
    created = Int()
    group_id = Int()
    uuid_finder = Unicode()
    uuid_loser = Unicode()
    workflow_state_id = Int()


class LafItemGroup(object):

    __export_to_model__ = True
    __storm_table__ = "item_group"

    id = Int(primary=True)
    name = Unicode()


class LafLocation(object):

    __export_to_model__ = True
    __storm_table__ = "location"

    id = Int(primary=True)
    place = Unicode()
    lat = Unicode()
    lng = Unicode()
    radius = Float()
    date_start = Int()
    date_end = Int()
    item_id = Int()


class LafChar(object):

    __export_to_model__ = True
    __storm_table__ = "characteristic"

    id = Int(primary=True)
    attr = Unicode()


class LafCharProp(object):

    __export_to_model__ = True
    __storm_table__ = "characteristic_property"

    id = Int(primary=True)
    value = Unicode()
    characteristic_id = Int()


class LafItemChar(object):

    __export_to_model__ = True
    __storm_table__ = "item_x_characteristic"
    __storm_primary__ = "item_id", "characteristic_id"

    item_id = Int()
    characteristic_id = Int()


def setup():
    from lascaux.model_setup import User, WorkflowState
    
    LafItem.group = Reference(LafItem.group_id, LafItemGroup.id)
    LafItem.finder = Reference(LafItem.uuid_finder, User.uuid)
    LafItem.loser = Reference(LafItem.uuid_loser, User.uuid)
    LafItem.state = Reference(LafItem.workflow_state_id, WorkflowState.id)
    LafItem.locations = ReferenceSet(LafItem.id, LafLocation.item_id)
    LafItem.characteristics = ReferenceSet(LafItem.id,
                                           LafItemChar.item_id,
                                           LafItemChar.characteristic_id,
                                           LafChar.id)

    LafChar.properties = ReferenceSet(LafChar.id,
                                      LafCharProp.characteristic_id)
