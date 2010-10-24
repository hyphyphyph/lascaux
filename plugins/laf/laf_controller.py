import time

try:
    import json
except:
    import simplejson as json

from lascaux import Controller

from lascaux.model import LafItem, LafItemGroup, WorkflowSet, Setting
from .item_forms import NewItemForm


class LafController(Controller):

    def _new_item(self, form):
        def new_item():
            setting = self.db.get(Setting, u"laf_item_workflow_set_id")
            workflowset = self.db.get(WorkflowSet, int(setting.value))
            group_name = form.group.value.strip().lower()
            group = self.db.find(LafItemGroup,
                                 LafItemGroup.name == group_name).one()
            if not group:
                group = LafItemGroup()
                group.name = group_name
                self.db.add(group)
                self.db.flush()
            item = LafItem()
            item.title = form.title.value
            item.kind = form.mode
            if self.user:
                setattr(item, "uuid_%s" % form.mode, self.user.uuid)
            item.created = int(time.time())
            item.workflow_state_id = workflowset.initial().id
            item.group_id = group.id
            self.db.add(item)
            self.db.flush()
            self.db.commit()
            return item
        self.add_js("new_item")
        if self.POST:
            form.ingest(self.POST)
            if form.validates():
                item = new_item()
                if (form.mode == "lost" and not item.uuid_loser) or \
                       (form.mode == "found" and not item.uuid_finder):
                    self.session["last_created_item_id"] = item.id
                    return self.redirect("user", "register")
                self.item = item
        self.save(form.render(self.render("new_item")))

    def new_lost(self):
        form = NewItemForm(self.route("new_lost"))
        form.setup(u"lost")
        return_ = self._new_item(form)
        if return_:
            return return_

    def new_found(self):
        form = NewItemForm(self.route("new_found"))
        form.setup(u"found")
        return_ = self._new_item(form)
        if return_:
            return return_

    def post_register(self, id):
        if "last_created_item_id" in self.session:
            self.session.unset("last_created_item_id")
        return "Thanks %s" % id

    def ajax_get_groups(self, term):
        groups = self.db.find(LafItemGroup)
        groups_ = {}
        for group in groups:
            if group.name.startswith(term.lower()):
                groups_[group.id] = {"name": group.name}
        return json.dumps(groups_)

    def quiz(self, group):
        item = self.db.get(LafItem, id)
        
