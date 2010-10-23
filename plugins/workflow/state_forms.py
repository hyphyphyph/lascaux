import string

from petrified import Form
from petrified.widgets import *


class NewStateForm(Form):

    __order__ = ["name", "title", "desc",
                 "prev", "next",
                 "submit"]

    name = Text(title="Name", required=True)
    title = Text(title="Title", required=True)
    desc = Text(title="Description", rows=4, cols=32)
    submit = Button(title="Create state")

    def populate_state_options(self, set):
        options = []
        for state in set.get_states():
            options.append((unicode(state.id), state.title))
        if options:
            options.insert(0, ("__none__", "(none)"))
            self.prev = Select(title="Previous State", options=options)
            self.next = Select(title="Next State", options=options)

    def validate(self):
        for c in self.name.value:
            if c not in string.ascii_lowercase + \
               "".join([unicode(i) for i in range(10)]) + u"_":
                self.name.error = True
                self.name.error_message = "Please choose a name that includes \
                                           only lowercase letters, numbers \
                                           and/or an underscore."
        if hasattr(self, "prev") and hasattr(self, "next"):
            self.prev.value = self.prev.value.isdigit() \
                    and int(self.prev.value) or self.prev.value
            self.next.value = self.next.value.isdigit() \
                    and int(self.next.value) or self.next.value
            if self.prev.value == "__none__":
                self.prev.value = 0
            if self.next.value == "__none__":
                self.next.value = 0
        if hasattr(self, "prev") and hasattr(self, "next") and \
           (self.prev.value != 0 or self.next.value != 0) \
           and self.prev.value == self.next.value:
            self.prev.error = True
            self.prev.error_message = "Improper workflow progression."
            self.next.error = True
            self.next.error_message = "Improper workflow progression."
            return False
        return True


class EditStateForm(NewStateForm):

    submit = Button(title="Save Changes")
