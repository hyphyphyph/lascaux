import re

from petrified.parser import Parser, ElementMatch


SELF_CLOSING_TAGS = ["input"]
CLOSING_TAGS = ["select", "textarea", "optgroup", "option", "label"]


class GSParser(Parser):
    """ Grunt Simple Parser """

    def find(self, name=""):
        if name:
            markup, start, end = self.find_named_element(name)
        if not markup or not start or not end:
            return None
        label = self.get_label_for(name)
        tag = self.get_tag(markup)
        if tag in SELF_CLOSING_TAGS:
            return ElementMatch(tag, markup, start, end,
                                name=name, label=label)
        elif tag in CLOSING_TAGS:
            regexp = "</%s>" % tag
            match = re.search(regexp, self.markup[start:], re.I)
            if not match:
                return None
            end = start+match.end()
            markup = self.markup[start:end+1]
            return ElementMatch(tag, markup, start, end,
                                name=name, label=label)

    def find_named_element(self, name):
        regexp = "name[ ]*=[ ]*\"%s\"" % name
        match = re.search(regexp, self.markup, re.I)
        if match:
            tag_start = self.markup.rfind("<", 0, match.start())
            tag_end = self.markup.find(">", match.end())
            tag_string = self.markup[tag_start:tag_end+1]
            return tag_string, tag_start, tag_end
        return False, False, False

    def get_label_for(self, name):
        regexp = "for[ ]*=[ ]*\"%s\"" % name
        match = re.search(regexp, self.markup, re.I)
        if match:
            start = self.markup.rfind("<", 0, match.start())
            end = self.markup.find("</label>", start)
            end += len("</label>")
            markup = self.markup[start:end+1]
            if start and end and markup:
                return ElementMatch("label", markup, start, end, for_=name)
        return None

    def get_tag(self, markup):
        return markup[1:].strip().split(" ")[0]
    
    def attr(self, match, attr, value=None):
        if not value:
            return self.get_attr(match, attr)
        return self.set_attr(match, attr, value)
    
    def set_attr(self, match, attr, value):
        match.altered_markup = hasattr(match, "altered_markup") and \
             match.altered_markup or match.markup
        regexp = "%s[ ]*=" % attr
        m = re.search(regexp, 
                      match.altered_markup[:match.altered_markup.find(">")+1], 
                      re.I)
        if not m:
            self._create_attr(match, attr, value)
        else:
            start = match.altered_markup.find('"', m.end())
            end = match.altered_markup.find('"', start+1)
            match.altered_markup = "%s%s%s" % (match.altered_markup[:start+1],
                                               value,
                                               match.altered_markup[end:])
    
    def _create_attr(self, match, attr, value):
        if match.tag in SELF_CLOSING_TAGS:
            match.altered_markup = '%s%s="%s" />' % (match.altered_markup[:-2], 
                                                     attr, value)
        elif match.tag in CLOSING_TAGS:
            end = match.altered_markup.find(">")
            start_tag = match.altered_markup[:end+1]
            start_tag = '%s %s="%s">' % (start_tag[:-1], attr, value)
            match.altered_markup = start_tag + match.altered_markup[end+1:]

    def append_attr(self, match, attr, value, sep=" "):
        match.altered_markup = hasattr(match, "altered_markup") and \
             match.altered_markup or match.markup
        regexp = "%s[ ]*=" % attr
        m = re.search(regexp, match.altered_markup, re.I)
        if not m:
            self._create_attr(match, attr, value)
        else:
            start = match.altered_markup.find('"', m.end())
            end = match.altered_markup.find('"', start+1)
            match.altered_markup = "%s%s%s%s" % (match.altered_markup[:end],
                                                 sep, value,
                                                 match.altered_markup[end:])
           
    def text(self, match, text):
        match.altered_markup = hasattr(match, "altered_markup") and \
             match.altered_markup or match.markup
        if match.tag in CLOSING_TAGS:
            start = match.altered_markup.find(">")
            end = match.altered_markup.rfind("</")
            match.altered_markup = "%s%s%s" % (match.altered_markup[:start+1],
                                               text,
                                               match.altered_markup[end:])

    def render(self, match):
        match.altered_markup = hasattr(match, "altered_markup") and \
             match.altered_markup or match.markup
        return match.altered_markup