import copy
import os.path

from crepehat import Kitchen
from mako.template import Template

from petrified import SObject, Widget, Environment, Parser


class Form(SObject):

    _form = None
    _action = "/"
    _method = "post"
    _properties = {}
    __order__ = []
    env = None

    def __init__(self, action="/", method=None, properties=None, env=None):
        self._form = self
        self._action = action
        self.env = env or Environment()
        if method and method.lower() in ("post", "get"):
            self._method = method
        if properties:
            self._properties = properties or {}
        for widget in self.list_widgets():
            setattr(self, widget.name, copy.copy(getattr(self, widget.name)))
        self.init()

    def init(self):
        pass

    def set_property(self, property, value):
        if property not in self._properties:
            self._properties[property] = u""
        self._properties[property] = value

    def get_property(self, property, default=None):
        if property in self._properties:
            return self._properties[property]
        return default

    def prop(self, property, default=None):
        return self.get_property(property, default)

    def get_root(self):
        form = self._form
        while form._form != form:
            form = form._form
        return form

    def list_widgets(self):
        if self.__order__:
            symbols = self.__order__
        else:
            symbols = []
            for symbol in dir(self):
                widget = getattr(self, symbol)
                if type(widget) == type(self): # type == instance
                    if issubclass(widget.__class__, Widget) and \
                       Widget in widget.__class__.__bases__:
                        symbols.append(symbol)
        widgets = []
        for symbol in symbols:
            if not hasattr(self, symbol):
                continue
            widget = getattr(self, symbol)
            widget.set_form(self)
            widget.name = symbol
            widgets.append(widget)
        return widgets

    def ingest(self, POST):
        for widget in self.list_widgets():
            widget.set_form(self)
            widget.ingest(POST.get(widget.name))
        return self

    def _validate(self):
        validity = []
        for widget in self.list_widgets():
            widget.validate()
        self.validate()
        for widget in self.list_widgets():
            validity.append(widget.error)
        return validity

    def validate(self):
        """A slightly kinder validate override..."""
        return True

    def validates(self):
        return not True in self._validate()

    def render(self, markup=None):
        if markup:
            p = Parser(markup)
            replacements = []
            for widget in self.list_widgets():
                e = p.find(name=widget.name)
                if e:
                    e.parser = p
                    markup_ = widget.render(e)
                    replacements.append((e, markup_ or ""))
            final_markup = None
            for i, r in enumerate(replacements):
                if final_markup == None:
                    final_markup = markup[:r[0].start] + r[1]
                else:
                    final_markup += "%s%s" % (
                        markup[replacements[i-1][0].end+1: r[0].start],
                        r[1]
                    )
            final_markup += markup[replacements[-1][0].end+1:]
            return final_markup
        markup = ""
        for widget in self.list_widgets():
            markup += widget.render()
        f = Kitchen(self.env.get_sources(), self.env.get_extensions())
        f = f.get("petrified/form")
        if not f:
            return markup
        t = Template(filename=f)
        return t.render(action=self._action, method=self._method,
                        properties=self._properties, content=markup)
