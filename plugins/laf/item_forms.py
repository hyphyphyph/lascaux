from petrified import Form
from petrified.widgets import *


class NewItemForm(Form):

    __order__ = ["title", "group", "pic", "submit"]

    mode = None

    title = Text(title="Title", required=True)
    group = Text(title="What is it?", required=True)
    pic = File(title="Photo", path="/tmp")
    submit = Button(title="Post it!")

    def setup(self, mode):
        self.mode = mode
        self.group.title = self.mode == "found" and \
                           "What did you find?" or \
                           self.mode == "lost" and \
                           "What did you lose?" or self.group.title
