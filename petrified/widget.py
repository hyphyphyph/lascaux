import weakref

from petrified.widgetmirror import WidgetMirror


class Widget(WidgetMirror):

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
    error = None
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

    def __getattr__(self, name):
        if name == 'value':
            print "123"
            if self.error == None:
                self.validate()
        return self.__dict__[name]

    def set_form_object(self, form):
        self._form = weakref.proxy(form.get_root_object())

    def get_form_object(self):
        return self._form.get_root_object()

    def render(self, markup=None):
        return markup or u''

    def ingest_POST(self, POST):
        self.error = None
        if self.name in POST:
            if type(POST.get(self.name)) is int:
                self.value = unicode(POST.get(self.name))
            else:
                self.value = POST.get(self.name).decode('utf-8')
        else:
            self.value = u''

    def validate(self):
        if self.value == None:
            self.value = u''
        self.error = False
        if self.required and not self.value:
            self.error = True
        return self.error

    def __str__(self):
        self._rendered = True
