import weakref


class Widget(object):

    _form = None
    _rendered = False

    name = None
    id = None
    classes= None
    title = None
    desc = None
    required = False
    disabled = False
    value = None
    error = False
    error_message = None

    def __init__(self, title=u'', value=None, required=False,
                 classes=None, id=None, disabled=False, name=u'',
                 error_message=None, desc=None):
        self.title = title
        self.desc = desc
        self.value = value
        self.required = required
        self.classes = classes or list()
        self.id = id
        self.disabled = disabled
        self.name = name
        self.error_message = error_message or u"You have to enter a value."

    def submit(self, values):
        if self.name in values:
            if type(values.get(self.name)) is int:
                self.value = unicode(values.get(self.name))
            else:
                self.value = values.get(self.name).decode('utf-8')
        self.validate()

    def validate(self):
        self.error = False
        if self.required and not self.value:
            self.error = True
        return self.error

    def render(self):
        self._rendered = True
        return u'<input type="hidden" name="%s" />' % self.name

    def is_rendered(self):
        return self._rendered

    def set_form(self, form):
        self._form = weakref.proxy(form.get_root_object())

    def __str__(self):
        return self.render()

    def __call__(self):
        return self.value
