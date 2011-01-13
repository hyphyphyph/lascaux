import os.path

from mako.template import Template
from crepehat import Kitchen

from petrified import Widget


class Password(Widget):

    size = None
    readonly = False

    def __init__(self, *argc, **argv):
        for key in ('size', 'readonly'):
            setattr(self, key, argv.get(key, getattr(self, key)))
            if key in argv:
                del argv[key]
        Widget.__init__(self, *argc, **argv)

    def export(self):
        desc = Widget.export(self)
        desc["size"] = self.size
        desc["readonly"] = self.readonly
        return desc

    def render(self, markup=None):
        Widget.render(self)
        f = Kitchen(self.get_form().get_widget_template_dirs(),
                    self.get_form().get_widget_template_extensions())
        f = f.get('password')
        if f:
            t = Template(filename=f)
            return t.render(**self.export())
        return u''
