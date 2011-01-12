class Mirror(object):

    something ="Derek"

    _mirror_mode = 'normal'
    _mirrored_attributes = list()

    def __init__(self):
        self._mirrored_attributes = list()
        self.make_accessible()

    def make_normal(self):
        self.__dict__['_mirror_mode'] = 'normal'

    def make_accessible(self):
        self.__dict__['_mirror_mode'] = 'accessible'

    def __getattr__(self, name):
        if self._mirror_mode == 'accessible':
            i = self.__get_named_attribute_index(name)
            if i >= 0:
                return self._mirrored_attributes[i][1]
        return self.__getattribute__(name)
            
    def __setattr__(self, name, value):
        if self._mirror_mode == 'accessible':
            i = self.__get_named_attribute_index(name)
            if i < 0:
                self._mirrored_attributes.append([name, value])
            else:
                self._mirrored_attributes[i][1] = value
        else:
            self.__dict__[name] = value
            
    def __get_named_attribute_index(self, name):
        sel = [i for i, attr in enumerate(self._mirrored_attributes)
               if attr[0] == name]
        if sel:
            return sel[0]
        return -1
