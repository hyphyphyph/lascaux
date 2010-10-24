import time

try:
    import json
except:
    import simplejson as json

from petrified import Form
from petrified.widgets import *

from lascaux import Controller

from lascaux.model import LafItem, LafItemGroup, LafLocation, \
     LafChar, WorkflowSet, Setting
from .item_forms import NewItemForm


class ContactForm(Form):

    __order__ = ["body", "send"]

    body = Text(title="Message", required=True, rows="16", cols="64")
    send = Button(title="Send Message")


class LafController(Controller):

    def _new_item(self, form):
        def new_item():
            setting = self.db.get(Setting, u"laf_item_workflow_set_id")
            workflowset = self.db.get(WorkflowSet, int(setting.value))
            group_name = form.group.value.strip(u" ").lower()
            group = self.db.find(LafItemGroup,
                                 LafItemGroup.name == group_name).one()
            if not group:
                group = LafItemGroup()
                group.name = group_name
                self.db.add(group)
                self.db.flush()

            # Create the item
            item = LafItem()
            item.kind = form.mode
            # If the user is already logged in, we can manage this straight away.
            if self.user:
                setattr(item, "uuid_%s" % (form.mode == "found" and "finder" or
                                           "loser"), self.user.uuid)
                item.workflow_state_id = workflowset.initial().next.id
            else:
                item.workflow_state_id = workflowset.initial().id
            item.created = int(time.time())
            item.group_id = group.id
            item = self.db.add(item)

            # Create the location
            location = LafLocation()
            location.place = form.place.value
            location.date_start = int(form.when_start.value)
            location.date_end = int(form.when_end.value)
            location = item.locations.add(location)

            if self.POST.get("characteristics_highest_index") != None:
                for i in xrange(
                    int(self.POST.get("characteristics_highest_index"))+1):
                    if self.POST.get("char_attr_%s" % i) and \
                       self.POST.get("char_val_%s" % i):
                        attr = self.POST.get("char_attr_%s" % i).decode("utf-8")
                        value = self.POST.get("char_val_%s" % i).decode("utf-8")
                        char = self.db.find(LafChar,
                                            LafChar.attr == attr,
                                            LafChar.value == value).one()
                        if not char:
                            char = LafChar()
                            char.attr = attr
                            char.value = value
                        self.db.add(char)
                        item.characteristics.add(char)

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
                self.save(self.render("thanks", {"item": item}))
                return True
        self.save(form.render(self.render("new_item", {"form": form})))

    def new_lost(self):
        self.save("lost", "form_mode")
        form = NewItemForm(self.route("new_lost"))
        form.setup(u"lost")
        return_ = self._new_item(form)
        if return_:
            return self.redirect("quiz", {"group": self.item.group.name})

    def new_found(self):
        self.save("found", "form_mode")
        form = NewItemForm(self.route("new_found"))
        form.setup(u"found")
        return_ = self._new_item(form)
        if return_:
            return return_

    def post_register(self, id):
        if "last_created_item_id" in self.session:
            self.session.unset("last_created_item_id")
        item = self.db.get(LafItem, id)
        self.save(self.render("thanks", {"item": item}))

    def thanks(self, id):
        item = self.db.get(LafItem, id)
        self.save(self.render("thanks", {"item": item}))

    def ajax_get_groups(self, term):
        groups = self.db.find(LafItemGroup)
        groups_ = {}
        for group in groups:
            if group.name.startswith(term.lower()):
                groups_[group.id] = {"name": group.name}
        return json.dumps(groups_)

    def quiz(self, group):
        self.save("form_mode", "lost")
        group = self.db.find(LafItemGroup, LafItemGroup.name == group).one()
        items = group.items
        chars = []
        for item in items:
            for char in item.characteristics:
                chars.append({"id": char.id,
                              "attr": char.attr,
                              "value": char.value,
                              "object": char})
        form = Form(self.route("quiz", {"group": group.name}))
        for char in chars:
            if char["attr"] not in form.__order__:
                setattr(form, char["attr"], Text(title=char["attr"]))
                form.__order__.append(char["attr"])
        form.__order__.append("submit")
        form.submit = Button(title="Narrow down the results...")
        form.carbonize()

        if self.POST:
            form.ingest(self.POST)
        results = {}
        for char in chars:
            attr = char["attr"]
            value = getattr(form, char["attr"]).value
            if value:
                chars_ = self.db.find(LafChar,
                                      LafChar.attr == attr,
                                      LafChar.value == value)
                for char_ in chars_:
                    for item in char_.items:
                        if item.id not in results:
                            results[item.id] = {"score": 0, "object": item}
                        results[item.id]["score"] += 1

        result_ids = [(r, results[r]["score"]) for r in results]
        def sort_by_score(k):
            return k[1]
        sorted(result_ids, key=sort_by_score)
        final_results = [results[r[0]]["object"] for r in result_ids]
        self.save(form.render(), "form_content")
        contact_form = ContactForm(self.route("send_message", {"group": group.name}))
        self.save(contact_form.render(), "contact_form")
        self.save(self.render("quiz", {"group": group,
                                       "characteristics": chars,
                                       "results": final_results}))

    def send_message(self):
        self.save(self.render("sent"))

    def welcome(self):
        self.save(self.render("welcome"))
