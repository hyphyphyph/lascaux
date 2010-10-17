from petrified import Form
from petrified.widgets import *


class NewIssueTypeForm(Form):

    __order__ = ["name", "title", "desc", "workflow", "submit"]

    name = Text(title="Name", required=True)
    title = Text(title="Title", required=True)
    desc = Text(title="Description", rows=4, cols=16)
    workflow = Select(title="Workflow")
    submit = Button(title="Create type")

    def populate_workflow_sets(self, project):
        options = []
        for set in project.workflow_sets:
            options.append((set.id, set.title))
        self.workflow.options = options

    def validate(self):
        self.workflow.value = int(self.workflow.value)
