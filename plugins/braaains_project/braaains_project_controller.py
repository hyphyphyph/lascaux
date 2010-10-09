from lascaux.model import *

from lascaux import Controller


class Braaains_ProjectController(Controller):

    def list(self):
        projects = self.db.find(Project)
        self.save(self.render("list", {"projects": projects}))

    def view(self, id):
        project = self.db.get(Project, id)
        blocks = {}
        self.hook("braaains_project_view", {"project": project,
                                            "blocks": blocks})
        self.save(self.render("view", {"project": project,
                                       "blocks": blocks}))
