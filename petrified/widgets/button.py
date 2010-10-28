import os.path

from mako.template import Template
from crepehat import Kitchen

from petrified import Widget


class Button(Widget):

    def __init__(self, title="", classes=None, id=None, disabled=False, 
                 name="", description=None):
        Widget.__init__(self,
                        title=title, value=None, required=False,
                        classes=classes, id=id, disabled=disabled,
                        name=name, description=description)

    def render(self, markup=None):
        f = Kitchen(self.get_form().env.get_sources(),
                    self.get_form().env.get_extensions())
        f = f.get(os.path.join("petrified", "button"))
        if f:
            t = Template(filename=f,
                         module_directory=self.get_form().env.get_tmpl_tmp())
            return t.render(**self.get_desc())
        return ""
