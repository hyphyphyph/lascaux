from lascaux import Controller


class LascauxController(Controller):
    def view(self, id):
        self.save("HERE I AM, VIEWING HERE I AM, VIEWING HERE I AM, VIEWING %s" % id)
