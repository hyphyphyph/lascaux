from storm.locals import *

from .asset_types import *


class Asset(object):

    __export_to_model__ = True
    __storm_table__ = "asset"

    id = Int(primary=True)
    created = Int()
    updated = Int()
    user_uuid = Unicode()
    title = Unicode()
    body = Unicode()
    type = Int()


class AssetType(object):

    __export_to_model__ = True
    __store_table__ = "asset_type"

    id = Int(primary=True)
    title = Unicode()
    desc = Unicode()
    enabled = Bool(default=True)
    has_file = Bool(default=False)
    has_vcs_file = Bool(default=False)
    has_page = Bool(default=False)
