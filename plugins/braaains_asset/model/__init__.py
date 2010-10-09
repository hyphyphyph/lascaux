from storm.locals import *

from lascaux.model import Project, User

from .asset_types import *


class Asset(object):

    __export_to_model__ = True
    __storm_table__ = "asset"

    id = Int(primary=True)
    created = Int()
    updated = Int()
    user_uuid = Unicode()
    user = Reference(user_uuid, User.uuid)
    title = Unicode()
    body = Unicode()
    type_id = Int()
    project_id = Int()
    project = Reference(project_id, Project.id)

Project.assets = ReferenceSet(Project.id, Asset.project_id)


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
    project = Reference(project_id, Project.id)


Asset.type = Reference(Asset.type_id, AssetType.id)
Project.asset_types = ReferenceSet(Project.id, AssetType.project_id)
