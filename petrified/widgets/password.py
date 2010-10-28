import os.path

from mako.template import Template
from crepehat import Kitchen

from petrified import Widget


class Password(Widget):

    cols = None
    rows = None
    readonly = False

    def __init__(self, title="", value=None, required=False,
                 classes=None, id=None, disabled=False, name="",
                 size=None, readonly=False, error_message=None,
                 description=None):
        Widget.__init__(self,
                        title=title, value=value, required=required,
                        classes=classes, id=id, disabled=disabled, name=name, 
                        error_message=error_message, description=description)
        self.size= size
        self.readonly = readonly

    def get_desc(self):
        d = Widget.get_desc(self)
        d["size"] = self.size
        d["readonly"] = self.readonly
        return d

    def render(self, markup=None):
        f = Kitchen(self.get_form().env.get_sources(),
                    self.get_form().env.get_extensions())
        f = f.get(os.path.join("petrified", "password"))
        if f:
            t = Template(filename=f,
                         module_directory=self.get_form().env.get_tmpl_tmp())
            return t.render(**self.get_desc())
        return ""
