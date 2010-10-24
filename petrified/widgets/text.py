import os.path

from mako.template import Template
from crepehat import Kitchen

from petrified import Widget, Parser


class Text(Widget):

    cols = None
    rows = None
    readonly = False

    def __init__(self, title="", value=None, required=False,
                 classes=None, id=None, disabled=False, name="",
                 cols=None, rows=None, readonly=False, error_message=None,
                 description=None):
        Widget.__init__(self,
                        title=title, value=value, required=required,
                        classes=classes, id=id, disabled=disabled, name=name, 
                        error_message=error_message, description=description)
        self.cols = cols
        self.rows = rows
        self.readonly = readonly

    def get_desc(self):
        d = Widget.get_desc(self)
        d["cols"] = self.cols
        d["rows"] = self.rows
        d["readonly"] = self.readonly
        return d

    def render(self, element=None):
        f = Kitchen(self.get_form().env.get_sources(),
                    self.get_form().env.get_extensions())
        f = f.get(os.path.join("petrified", "text"))
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
        if self.readonly:
            p.attr(e, "readonly", "readonly")
        e_markup = p.render(e)
        return rendered[0:e.start] + e_markup + rendered[e.end+1:]
