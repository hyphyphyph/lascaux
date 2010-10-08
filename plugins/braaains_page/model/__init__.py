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

    id = Int()
    vid = Int(primary=True)
    title = Unicode()
    body = Unicode()
    format = Unicode()
    created = Int()
    user_uuid = Unicode()
