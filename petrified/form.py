import os.path

from mako.template import Template

from petrified.mirror import Mirror
from petrified.widget import Widget


class Form(Mirror):

    _opened = False

    template = 'templates/form.mako'
    action = '/'
    method = 'post'
    attributes = dict()
    form = None
    started = False

    def __init__(self, action='/', method=None, *argc, **argv):
        self._form = self # weakref resolution
        if os.path.abspath(self.template) != self.template:
            self.template = os.path.abspath(
                os.path.join(os.path.dirname(__file__), self.template))
        self._rendered_widget_names = list()
        self.action = action
        if method and method.lower() in ("post", "get"):
            self.method = method
        self.attributes = dict()
        for key in argv:
            self._attributes[key] = argv[key]
        Mirror.__init__(self)
        self.__setup__()

    def __setup__(self):
        pass

    def attr(self, name, value=None):
        if value != None:
            self.attributes[name] = value
        return self.attributes.get(name, value)

    def submit(self, values):
        self.make_accessible()
        for widget in self.widgets:
            widget.ingest(post.get(widget.name))

    def _validates(self):
        validates = True
        for widget in self.widgets:
            widget.validate()
        if not self.check_validates():
            validates = False
        if [False for widget in self.widgets if widget.error]:
            validates = False
        return validates
    validates = _validates

    def open(self):
        self._opened = True
        return self.render(only_header=True)

    def render(self, only_header=False):
        if os.path.isfile(self.template):
            t = Template(filename=self.template)
            return t.render(form=self,
                            only_header=only_header).encode('utf-8')
        return u''

    def __str__(self):
        return self.render()

    def get_widgets(self):
        return [w['value'] for w in self.get_mirrored_attributes()]
    widgets = property(get_widgets)

    def get_unrendered_widgets(self):
        return [w['value'] for w in self.get_mirrored_attributes() 
                if not w['value'].is_rendered()]
    unrendered_widgets = property(get_unrendered_widgets)

    def _on_new_setattr(self, name, widget):
        if widget.__class__ == Widget or \
           Widget in widget.__class__.__bases__:
            widget.name = name
            widget.set_form(self)
        
    def get_root_object(self):
        form = self._form
        while form._form != form:
            form = form._form
        return form

    def is_open(self):
        return self._opened
