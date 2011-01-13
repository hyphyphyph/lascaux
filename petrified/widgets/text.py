import os.path

from mako.template import Template
from crepehat import Kitchen

from petrified import Widget


class Text(Widget):

    cols = None
    rows = None
    readonly = False

    def __init__(self, *argc, **argv):
        for key in ('cols', 'rows', 'readonly'):
            setattr(self, key, argv.get(key, getattr(self, key)))
            if key in argv:
                del argv[key]
        Widget.__init__(self, *argc, **argv)

    def render(self, element=None):
        Widget.render(self)
        f = Kitchen(self.get_form().get_widget_template_dirs(),
                    self.get_form().get_widget_template_extensions())
        f = f.get("text")
        if f:
            t = Template(filename=f)
            return t.render(**self.export())
        return u''

    def export(self):
        desc = Widget.export(self)
        desc['cols'] = self.cols
        desc['rows'] = self.rows
        desc['readonly'] = self.readonly
        return desc
