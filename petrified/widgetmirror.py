class WidgetMirror(object):

    _widgets = list()
    _mirror_mode = False

    def __init__(self):
        self._widgets = list()

    def _get_widgets(self):
        """should return a list of the widgets"""
        return self._widgets
    widgets = property(_get_widgets)

    def __getattr__(self, name):
        if self.is_widget_mode and name in [w.name
                                            for w in self.widgets]:
            return [w for w in self.widgets if w.name == name][0]
        elif name in self.__dict__:
            return self.__dict__[name]
        else:
            raise AttributeError(u"%s instance has no attribute '%s'" %
                                 (self.__class__.__name__, name))

    def __setattr__(self, name, value):
        if name == "started":
            print self.__dict__
        if self.is_widget_mode and name not in self.__dict__:
            value.name = name
            if name not in [w.name for w in self.widgets]:
                self.append_widget(value)
            else:
                widget = [w for w in self.widget if w.name == name][0]
                widget = value
        else:
            self.__dict__[name] = value
        
    def append_widget(self, widget):
        self.widgets.append(widget)

    def widget_mode(self, state=True):
        self._mirror_mode = state
        return self._mirror_mode

    def get_widget_mode(self):
        return self._mirror_mode
    is_widget_mode = property(get_widget_mode)

    def normal_mode(self, state=True):
        self._mirror_mode = not state
        return not self._mirror_mode

    def get_normal_mode(self):
        return not self._mirror_mode
    is_normal_mode = property(get_normal_mode)
