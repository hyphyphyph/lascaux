import re


class Parser(object):
    
    markup = None
    
    def __init__(self, markup):
        self.markup = markup


class ElementMatch(object):

    tag = None
    name = None
    for_ = None
    markup = None
    start = None
    end = None
    label = None

    def __init__(self, tag, markup, start, end,
                 name=None, for_=None, label=None):
        self.tag = tag
        self.markup = markup
        self.start = start
        self.end = end
        self.label = label
        self.name = name
        self.for_ = for_