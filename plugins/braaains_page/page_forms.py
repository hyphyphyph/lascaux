from petrified import Form
from petrified.widgets import *


class NewPageForm(Form):

    __order__ = ["title", "body", "save"]

    title = Text(title="Title", required=True)
    body = Text(title="Body", required=True, rows=20)
    save = Button(title="Save Page")
