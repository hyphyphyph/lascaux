from petrified import Form
from petrified.widgets import *


class PageForm(Form):

    __order__ = ["title", "body", "save"]

    title = Text(title="Title", required=True)
    body = Text(title="Body", required=True, rows=16, cols=128)
    save = Button(title="Save Page")
