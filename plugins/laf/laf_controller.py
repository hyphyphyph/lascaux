import time

from lascaux import Controller

from lascaux.model import LafItem, LafItemGroup
from .item_forms import NewItemForm


class LafController(Controller):

    def _new_item(self, form):
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
        item.kind = form.prop("mode")
        item.created = int(time.time())
        item.group_id = group.id
        self.db.add(item)
        self.db.flush()
        self.db.commit()
        return item

    def new_lost(self):
        form = NewItemForm(self.route("new_lost"))
        form.setup(u"lost")
        if self.POST:
            form.ingest(self.POST)
            if form.validates():
                item = self._new_item(form)
                return self.redirect("new_lost")
        self.save(form.render())

    def new_found(self):
        form = NewItemForm(self.route("new_found"))
        form.setup(u"found")
        if self.POST:
            form.ingest(self.POST)
            if form.validates():
                item = self._new_item(form)
                return self.redirect("new_found")
        self.save(form.render())
