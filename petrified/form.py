import os.path

from mako.template import Template

from petrified.widgetmirror import WidgetMirror


class Form(WidgetMirror):

    form_template = None
    action = "/"
    method = "post"
    attributes = dict()
    _form = None

    def __init__(self, action="/", method=None, *argc, **argv):
        self._form = self # weakref resolution
        self._widgets = list()
        self.attributes = dict()
        self.action = action1+
        if method and method.lower() in ("post", "get"):
            self.method = method
        for key in argv:
            if key == 'markup':
                self.ingest_markup(argv[key])
            elif key == 'POST':
                self.ingest_POST(argv[key])
            else:
                self._attributes[key] = argv[key]
        self.__define__()

    def get_root_object(self):
        form = self._form
        while form._form != form:
            form = form._form
        return form

    def __define__(self):
        pass

    def attr(self, name, value=None):
        if value != None:
            self.attributes[name] = value
        return self.attributes.get(name, value)

    def val(self, name, value=None):
        if value != None:
            if name in self.widgets:
                self.widgets[name].value = value
        if name in self.widgets:
            return self.widgets[name].value

    def ingest_POST(self, POST):
        self.widget_mode()
        for widget in self.widgets:
            widget.set_form(self)
            widget.ingest(POST.get(widget.name))

    def ingest_markup(self):
        pass

    def _check_validates(self):
        validates = True
        for widget in self.widgets:
            widget.validate()
        if not self.check_validates():
            validates = False
        if [False for widget in self.widgets if widget.error]):
            validates = False
        return validates
    is_valid = property(_check_validates)

    def check_validates(self):
        return True

    def render(self):
        pass

    def __str__(self):
        # # TODO: find the file
        # t = Template(filename=file_, module_directory=os.path.join(
        #     config.get_tmp(), 'tmpl_cache'))
        # rendered = t.render(form=self, widgets=form.widgets).encode('utf-8')
        return unicode(self.name)
