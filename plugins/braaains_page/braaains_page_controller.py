from lascaux.model import Page, PageVersion

from lascaux import Controller

from .page_forms import *


class Braaains_PageController(Controller):

    def view(self, id):
        page = self.db.get(Page, id)
        self.save(self.render("view", {"page": page}))

    def new(self, id):
        form = NewPageForm(self.route("new", {"id": id}))
        if self.POST:
            form.ingest(self.POST)
            if not form.validates():
                return self.save(form.render())
            else:
                version = PageVersion()
                version.title = form.title().value
                version.body = form.body().value
                version.user_uuid = u"abc"
                version.created = 1
                version.format = u"html"
                self.db.add(version)
                self.db.flush()

                page = Page()
                page.vid = version.vid
                page.user_uuid = u"abc"
                page.created = 1
                page.updated = 1
                page.enabled = True
                page.project_id = id
                self.db.add(page)
                self.db.flush()

                version.page_id = page.id
                self.db.add(version)
                self.db.flush()
                return self.redirect("view", {"id": page.id})
        self.save(form.render())
