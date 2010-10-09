from storm.locals import *

from .__init__ import Asset


class AssetResourceFile(object):

    __export_to_model__ = True
    __store_table__ = "asset_resoure_file"

    id = Int(primary=True)
    path = Unicode()
    created = Int()
    asset_id = Int()
    asset = Reference(asset_id, Asset.id)


class AssetResourcePage(object):

    __export_to_model__ = True
    __store_table__ = "asset_resoure_page"

    id = Int(primary=True)
    page_id = Int()
    created = Int()
    asset_id = Int()
    asset = Reference(asset_id, Asset.id)


Asset.resource_file = Reference(Asset.id, AssetResourceFile.asset_id)
Asset.resource_page = Reference(Asset.id, AssetResourcePage.asset_id)
