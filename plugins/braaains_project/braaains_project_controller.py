from lascaux.model import *

from petrified import Form

from .project_forms import NewForm

from lascaux import Controller


class Braaains_ProjectController(Controller):

    def list(self):
        projects = self.db.find(Project)
        self.save(self.render("list", {"projects": projects}))

    def view(self, id):
        project = self.db.get(Project, id)
        if project:
            blocks = {}
            self.hook("braaains_project_view", {"project": project,
                                                "blocks": blocks})
            self.save(self.render("view", {"project": project,
                                           "blocks": blocks}))

    def new(self):
        form = NewForm(self.route("new"))
        if self.POST:
            form.ingest(self.POST)
            if form.validates():
                project = Project()
                project.title = form.title.value
                project.desc = form.desc.value
                self.db.add(project)
                self.db.flush()
                return self.redirect("view", {"id": project.id})
        self.save(form.render(), "form_content")
        self.save(self.render("new"))
