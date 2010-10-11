import time

from lascaux.model import Page, PageVersion

from lascaux import Controller

from .page_forms import *


class Braaains_PageController(Controller):

    def view(self, id):
        page = self.db.get(Page, id)
        self.save(self.render("view", {"page": page}))

    def new(self, project_id):
        form = PageForm(self.route("new", {"project_id": project_id}))
        if self.POST:
            form.ingest(self.POST)
            if not form.validates():
                return self.save(form.render())
            else:
                version = PageVersion()
                version.title = form.title().value
                version.body = form.body().value
                version.user_uuid = self.user and self.user.uuid or u""
                version.created = int(time.time())
                version.format = u"html"
                self.db.add(version)
                self.db.flush()

                page = Page()
                page.vid = version.vid
                page.user_uuid = self.user and self.user.uuid or u""
                page.created = int(time.time())
                page.updated = int(time.time())
                page.enabled = True
                page.project_id = project_id
                self.db.add(page)
                self.db.flush()

                version.page_id = page.id
                self.db.add(version)
                self.db.flush()
                return self.redirect("view", {"id": page.id})
        self.save(form.render())

    def edit(self, id):
        page = self.db.get(Page, id)
        form = PageForm(self.route("edit", dict(id=id)))
        if self.POST:
            form.ingest(self.POST)
            if form.validates():
                if page.version.title != form.title().value or \
                   page.version.body != form.body().value:
                    version = PageVersion()
                    version.page_id = page.id
                    version.title = form.title().value
                    version.body = form.body().value
                    version.created = int(time.time())
                    version.format = form.body().value.startswith("<") and u"html" or u"raw"
                    version.user_uuid = self.user and self.user.uuid or u""
                    self.db.add(version)
                    self.db.flush()

                    page.vid = version.vid
                    self.db.add(page)
                    self.db.flush()
                return self.redirect("view", dict(id=id))
        else:
            form.title.value = page.version.title
            form.body.value = page.version.body
            self.save(form.render())
