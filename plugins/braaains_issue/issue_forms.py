from petrified import Form
from petrified.widgets import *


class NewIssueForm(Form):

    __order__ = ["type", "title", "body", "submit"]

    type = Select(title="Issue Type")
    title = Text(title="Title/Subject", required=True)
    body = Text(title="Details", rows=8, cols=128)
    submit = Button(title="Create")

    def populate_issue_types(self, project):
        options = []
        for type_ in project.issue_types:
            options.append((type_.id, type_.title))
        self.type.options = options

    def validate(self):
        self.type.value = int(self.type.value)
