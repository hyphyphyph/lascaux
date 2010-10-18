from storm.locals import *


class Page(object):

    __export_to_model__ = True
    __storm_table__ = "page"

    id = Int(primary=True)
    vid = Int()
    user_uuid = Unicode()
    created = Int()
    updated = Int()
    enabled = Bool(default=True)
    project_id = Int()


class PageVersion(object):

    __export_to_model__ = True
    __storm_table__ = "page_version"

    page_id = Int()
    vid = Int(primary=True)
    title = Unicode()
    body = Unicode()
    format = Unicode()
    created = Int()
    user_uuid = Unicode()


def setup():
    from lascaux.model_setup import User, Project

    Page.user = Reference(Page.user_uuid, User.uuid)
    Page.project = Reference(Page.project_id, Project.id)
    Page.version = Reference(Page.vid, PageVersion.vid)

    PageVersion.user = Reference(PageVersion.user_uuid, User.uuid)
    PageVersion.page = Reference(PageVersion.page_id, Page.id)

    Project.pages = ReferenceSet(Project.id, Page.project_id)
