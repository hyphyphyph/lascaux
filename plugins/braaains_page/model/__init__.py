from storm.locals import *

from lascaux.model_setup import User, Project
# from plugins.braaains_project.model import Project


class Page(object):

    __export_to_model__ = True
    __storm_table__ = "page"

    id = Int(primary=True)
    vid = Int()
    user_uuid = Unicode()
    user = Reference(user_uuid, User.uuid)
    created = Int()
    updated = Int()
    enabled = Bool(default=True)
    project_id = Int()
    project = Reference(project_id, Project.id)


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
    user = Reference(user_uuid, User.uuid)


def setup():
    Page.version = Reference(Page.vid, PageVersion.vid)
    PageVersion.page = Reference(PageVersion.page_id, Page.id)
    Project.pages = ReferenceSet(Project.id, Page.project_id)
