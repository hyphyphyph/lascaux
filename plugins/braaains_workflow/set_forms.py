from petrified import Form
from petrified.widgets import *


class NewSetForm(Form):

    __order__ = ["title", "desc", "submit"]

    title = Text(title="Title", required=True)
    desc = Text(title="Description", rows=16, cols=128)
    submit = Button(title="Create Set")


class EditSetForm(NewSetForm):

    submit = Button(title="Save Changes")
