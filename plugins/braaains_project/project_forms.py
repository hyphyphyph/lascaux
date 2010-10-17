from petrified import Form
from petrified.widgets import *


class NewForm(Form):

    __order__ = ["title", "desc", "save"]

    title = Text(title="Title", required=True)
    desc = Text(title="Description", rows=16, cols=128)
    save = Button(title="Create new page")
