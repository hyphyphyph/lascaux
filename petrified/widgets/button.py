import os.path

from mako.template import Template
from crepehat import Kitchen

from petrified import Widget


class Button(Widget):

    def render(self):
        Widget.render(self)
        f = Kitchen(self.get_form().get_widget_template_dirs(),
                    self.get_form().get_widget_template_extensions())
        f = f.get("button")
        if f:
            t = Template(filename=f)
            return t.render(**self.export())
        return u''
