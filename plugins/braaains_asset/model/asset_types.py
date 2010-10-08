from storm.locals import *


class AssetResourceFile(object):

    __export_to_model__ = True
    __store_table__ = "asset_resoure_file"

    id = Int(primary=True)
    path = Unicode()
    created = Int()


class AssetResourcePage(object):

    __export_to_model__ = True
    __store_table__ = "asset_resoure_page"

    id = Int(primary=True)
    page_id = Int()
    created = Int()
