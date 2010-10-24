import os.path

from mako.template import Template
from crepehat import Kitchen

from petrified import Widget, Parser


class Select(Widget):

    options = {}

    def __init__(self, title="", options=None, value=None, required=False,
                 classes=None, id=None, disabled=False, name="",
                 cols=None, rows=None, readonly=False, error_message=None,
                 description=None):
        Widget.__init__(self,
                        title=title, value=value, required=required,
                        classes=classes, id=id, disabled=disabled, name=name,
                        error_message=error_message, description=description)
        self.options = options or {}

    def get_desc(self):
        d = Widget.get_desc(self)
        d["options"] = self.options
        return d

    def render(self, element=None):
        f = Kitchen(self.get_form().env.get_sources(),
                    self.get_form().env.get_extensions())
        f = f.get(os.path.join("petrified", "select"))
        if f:
            t = Template(filename=f, module_directory=self.get_form(). \
                         env.get_tmpl_tmp())
            rendered = t.render(**self.get_desc())
        if not element:
            return rendered
        p = Parser(rendered)
        e = p.find(name=self.name)
        if not e:
            return rendered
        self.apply_desc(p, e)
        e_markup = p.render(e)
        return rendered[0:e.start] + e_markup + rendered[e.end+1:]
