from lascaux import model
from lascaux import Controller

from .set_forms import *
from .state_forms import *


class WorkflowController(Controller):

    def new_set(self):
        form = NewSetForm(self.route("new_set"))
        if self.POST:
            form.ingest(self.POST)
            if form.validates():
                set = model.WorkflowSet()
                set.title = form.title.value
                set.desc = form.desc.value
                self.db.add(set)
                self.db.flush()
                self.db.commit()
                return self.redirect("view_set", {"id": set.id})
        self.save(form.render(), "form_content")
        self.save(self.render("new_set"))

    def view_set(self, id):
        set = self.db.get(model.WorkflowSet, id)
        self.save(self.render("view_set", {"set": set,
                                           "states": set.get_states()}))

    def edit_set(self, id):
        set = self.db.get(model.WorkflowSet, id)
        form = EditSetForm(self.route("edit_set", {"id": id}))
        if self.POST:
            form.ingest(self.POST)
            if form.validates():
                set.title = form.title.value
                set.desc = form.desc.value
                return self.redirect("view_set", {"id": id})
        else:
            form.title(set.title)
            form.desc(set.desc)
        self.save(form.render(), "form_content")
        self.save(self.render("edit_set"))

    def new_state(self, set_id):
        set = self.db.get(model.WorkflowSet, set_id)
        form = NewStateForm(self.route("new_state", {"set_id": set_id}))
        form.populate_state_options(set)
        if self.POST:
            form.ingest(self.POST)
            if form.validates():
                update_first = False
                if set.states.count() == 1:
                    update_first = True
                    first = set.states.one()
                state = model.WorkflowState()
                state.workflow_set_id = set_id
                state.name = form.name.value
                state.title = form.title.value
                state.desc = form.desc.value
                state.prev_id = hasattr(form, "prev") and form.prev.value
                state.next_id = hasattr(form, "next") and form.next.value
                self.db.add(state)
                self.db.flush()
                self.db.commit()
                if update_first:
                    first.next_id = state.id
                    self.db.add(first)
                    self.db.flush()
                    self.db.commit()
                return self.redirect("view_set", {"id": set_id})
        self.save(form.render())

    def edit_state(self, id):
        state = self.db.get(model.WorkflowState, id)
        form = EditStateForm(self.route("edit_state", {"id": id}))
        form.populate_state_options(state.set)
        if self.POST:
            form.ingest(self.POST)
            if form.validates():
                state.name = form.name.value
                state.title = form.title.value
                state.desc = form.desc.value
                state.prev = form.prev.value
                state.next = form.next.value
                self.db.add(state)
                self.db.flush()
                self.db.commit()
                return self.redirect("view_set", {"id": state.set.id})
        form.name(state.name)
        form.title(state.title)
        form.desc(state.desc)
        form.prev(state.prev_id)
        form.next(state.next_id)
        self.save(form.render())
