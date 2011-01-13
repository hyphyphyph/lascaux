import os.path

from mako.template import Template
from crepehat import Kitchen

from petrified import Widget


class Select(Widget):

    options = {}

    def __init__(self, *argc, **argv):
        self.options = argv.get("options", {})
        if 'options' in argv:
            del argv['options']
        Widget.__init__(self, *argc, **argv)

    def export(self):
        desc = Widget.export(self)
        desc["options"] = self.options
        return desc

    def render(self, element=None):
        Widget.render(self)
        f = Kitchen(self.get_form().get_widget_template_dirs(),
                    self.get_form().get_widget_template_extensions())
        f = f.get("select")
        if f:
            t = Template(filename=f)
            return t.render(**self.export())
        return u''
