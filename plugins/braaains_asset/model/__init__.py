from storm.locals import *


class Asset(object):

    __export_to_model__ = True
    __storm_table__ = "asset"

    id = Int(primary=True)
    created = Int()
    updated = Int()
    user_uuid = Unicode()
    title = Unicode()
    body = Unicode()
    type_id = Int()
    project_id = Int()


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
    project_id = Int()


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


def setup():
    from lascaux.model_setup import Project, User

    Asset.user = Reference(Asset.user_uuid, User.uuid)
    Asset.project = Reference(Asset.project_id, Project.id)

    AssetType.project = Reference(AssetType.project_id, Project.id)

    Project.assets = ReferenceSet(Project.id, Asset.project_id)
    Asset.type = Reference(Asset.type_id, AssetType.id)
    Project.asset_types = ReferenceSet(Project.id, AssetType.project_id)

    Asset.resource_file = Reference(Asset.id, AssetResourceFile.asset_id)
    Asset.resource_page = Reference(Asset.id, AssetResourcePage.asset_id)
