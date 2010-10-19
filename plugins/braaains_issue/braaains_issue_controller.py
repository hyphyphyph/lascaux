import time

from lascaux import model

from lascaux import Controller

from .issue_forms import *
from .type_forms import *


class Braaains_IssueController(Controller):

    def list(self, project_id):
        project = self.db.get(model.Project, project_id)
        self.save(self.render("list", {"project": project,
                                       "issues": [i for i in project.issues]}))

    def view(self, id):
        issue = self.db.get(model.Issue, id)
        self.save(self.render("comments", {"issue": issue,
                                           "comments": issue.comments}),
                  "comments")
        self.save(self.render("issue", {"issue": issue}))

    def new(self, project_id):
        project = self.db.get(model.Project, project_id)
        form = NewIssueForm(self.route("new", {"project_id": project_id}))
        form.populate_issue_types(project)
        if self.POST:
            form.ingest(self.POST)
            if form.validates():
                issue = model.Issue()
                issue.project_id = project_id
                issue.issue_type_id = form.type.value
                issue.title = form.title.value
                issue.body = form.body.value
                type_ = self.db.get(model.IssueType, form.type.value)
                state = type_.workflow_set.get_states()[0]
                issue.workflow_state_id = state.id
                issue.user_uuid = self.user.uuid
                issue.created = int(time.time())
                self.db.add(issue)
                self.db.flush()
                return self.redirect("list", {"project_id": project_id})
        self.save(form.render())

    def new_type(self, project_id):
        project = self.db.get(model.Project, project_id)
        form = NewIssueTypeForm(self.route("new_type",
                                           {"project_id": project_id}))
        form.populate_workflow_sets(project)
        if self.POST:
            form.ingest(self.POST)
            if form.validates():
                type_ = model.IssueType()
                type_.name = form.name.value
                type_.title = form.title.value
                type_.desc = form.desc.value
                type_.project_id = project_id
                type_.workflow_set_id = form.workflow.value
                self.db.add(type_)
                self.db.flush()
                return self.redirect("list", {"project_id": project_id})
        self.save(form.render())
