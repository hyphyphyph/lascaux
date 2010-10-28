class BaseSelector:

    parameter = None

    def __init__(self, Parameter):
        self.parameter = Parameter

    def test(self, Against):
        pass


class EQUALS(BaseSelector):
    def test(self, Against):
        if Against == self.parameter:
            return True
        return False


class IN(BaseSelector):
    def __init__(self, Parameter):
        if not hasattr(Parameter, "__iter__"):
            Parameter = [Parameter]
        BaseSelector.__init__(self, Parameter)

    def test(self, Against):
        if not hasattr(Against, "__iter__"):
            Against = [Against]
        for item in Against:
            if item in self.parameter:
                return True
        return False


class ALL(IN):
    def test(self, Against):
        if not hasattr(Against, "__iter__"):
            Against = [Against]
        all_ = []
        for parameter in self.parameter:
            if parameter not in Against:
                all_.append(False)
        return not False in all_
