from lascaux.model import Setting

from lascaux import Controller

from petrified import Form
from petrified.widgets import *


class SettingsEditForm(Form):

    __order__ = ["save"]

    save = Button(title="Save")


class SettingNewForm(Form):

    __order__ = ["name", "value", "submit"]

    name = Text(title="Name", required=True)
    value = Text(title="Value", required=True)
    submit = Button(title="Save")


class SettingController(Controller):

    def index(self):
        form = SettingsEditForm(self.route("index"))
        settings = self.db.find(Setting)
        for setting in settings:
            form.__order__.insert(0, setting.name)
            setattr(form, setting.name, Text(title=setting.name,
                                             value=setting.value))
        if self.POST:
            form.ingest(self.POST)
            if form.validates():
                for setting in settings:
                    if setting.value != getattr(form, setting.name).value:
                        setting.value = getattr(form, setting.name).value
                        self.db.add(setting)
                self.db.flush()
                self.db.commit()
        self.save(form.render(), "edit_form")
        self.save(self.render("settings"))

    def new(self):
        form = SettingNewForm(self.route("new"))
        if self.POST:
            form.ingest(self.POST)
            if form.validates():
                setting = Setting()
                setting.name = form.name.value
                setting.value = form.value.value
                self.db.add(setting)
                self.db.flush()
                self.db.commit()
                return self.redirect("index")
        self.save(form.render())
