class SelectionList:

    selection = []

    def __init__(self, Set):
        try:
            self.selection = Set.__iter__ and Set
        except:
            raise TypeError('%s parameter "Set" must be an iterable!' % \
                  self.__class__.__name__)

    def append(self, Item):
        self.selection.append(Item)

    def select(self, Key, Selector):
        selection = []
        for item in self.selection:
            if type(item) == type({}):
                properties = item.get(Key)
            else:
                properties = getattr(item, Key)
            if Selector.test(properties):
                selection.append(item)
        sl = SelectionList(selection)
        return sl

    def __iter__(self):
        return self.selection.__iter__()

    def __len__(self):
        return len(self.selection)

    def __contains__(self, Value):
        return Value in self.selection

    def __getitem__(self, Key):
        return self.selection[Key]

    def __str__(self):
        return self.selection.__str__()

    def __repr__(self):
        return self.selection.__repr__()

    def __delitem__(self, key):
        del self.selection[key]
