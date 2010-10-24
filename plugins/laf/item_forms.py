from petrified import Form
from petrified.widgets import *


class NewItemForm(Form):

    __order__ = ["group", "picture", "place", "when_start", "when_end",
                 "title", "submit"]

    mode = None

    group = Text(title="What is it?", required=True)
    picture = File(title="Photo")
    place = Text(title="Where?")
    when_start = Text(title="When?")
    when_end = Text(title="When?")
    title = Text(title="Title", required=True)
    submit = Button(title="Post it!")

    def setup(self, mode):
        self.mode = mode
        self.group.title = self.mode == "found" and \
                           "What did you find?" or \
                           self.mode == "lost" and \
                           "What did you lose?" or self.group.title
