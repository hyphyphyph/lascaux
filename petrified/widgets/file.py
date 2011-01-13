import os
import os.path

from mako.template import Template
from crepehat import Kitchen

from petrified import Widget


class File(Widget):

    path = None

    def __init__(self, *argc, **argv):
        self.path = argv.get('path', self.path)
        if "path" in argv:
            del argv["path"]
        Widget.__init__(self, *argc, **argv)

    def export(self):
        desc = Widget.export(self)
        desc["path"] = self.path
        return desc

    def render(self):
        Widget.render(self)
        f = Kitchen(self.get_form().get_widget_template_dirs(),
                    self.get_form().get_widget_template_extensions())
        f = f.get("file")
        if f:
            t = Template(filename=f)
            return t.render(**self.export())
        return u''

    def set_form(self, form):
        Widget.set_form(self, form)
        form.attr("enctype", "multipart/form-data")

    def submit(self, value):
        self.value = value
        if self.path and self.value:
            os.rename(self.value, os.path.join(self.path,
                                               os.path.basename(self.value)))
