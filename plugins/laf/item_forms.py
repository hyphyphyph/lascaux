from petrified import Form
from petrified.widgets import *


class NewItemForm(Form):

    __order__ = ["group", "place", "when_start", "when_end", "submit"]

    mode = None

    group = Text(title="I lost", required=True, value="laptop, camera, purse")
    place = Text(title="Search a place")
    when_start = Text(title="From")
    when_end = Text(title="To")
    submit = Button(title="Post it!")

    def setup(self, mode):
        self.mode = mode
        self.group.title = self.mode == "found" and \
                           "What did you find?" or \
                           self.mode == "lost" and \
                           "I lost..." or self.group.title
