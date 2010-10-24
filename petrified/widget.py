import weakref

from petrified import SObject, Parser


class Widget(SObject):

    _form = None
    name = None
    id = None
    classes = None
    title = None
    description = None
    required = False
    disabled = False
    value = None
    error = False
    error_message = None

    def __init__(self, title="", value=None, required=False,
                 classes=None, id=None, disabled=False, name="",
                 error_message=None, description=None):
        self.title = title
        self.description = description
        self.value = value
        self.required = required
        self.classes = classes or []
        self.id = id
        self.disabled = disabled
        self.name = name
        self.error_message = error_message or "You have to enter a value."

    def __call__(self, value=None):
        if value != None:
            self.ingest(value)
        if self.error == None:
            self.validate()
        return self

    def set_form(self, form):
        self._form = weakref.proxy(form.get_root())

    def get_form(self):
        return self._form.get_root()

    def get_desc(self):
        return {
            "name": self.name,
            "id": self.id,
            "classes": " ".join(self.classes),
            "title": self.title,
            "description": self.description,
            "required": self.required,
            "disabled": self.disabled,
            "value": self.value,
            "error": self.error,
            "error_message": self.error_message
        }

    def apply_desc(self, parser, element):
        d = self.get_desc()
        if d["disabled"]:
            parser.attr(element, "disabled", "disabled")
        if d["id"]:
            parser.attr(element, "id", d["id"])
        if d["classes"]:
            parser.append_attr(element, "class", d["classes"])

    def render(self, markup=None):
        return markup or ""

    def ingest(self, value):
        if value:
            if type(value) is int:
                self.value = unicode(value)
            else:
                self.value = type(value.decode("utf-8"))
        else:
            self.value = u""

    def validate(self):
        if self.required and not self.value:
            self.error = True
        return self.error
