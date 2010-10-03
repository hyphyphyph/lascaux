from lascaux.model import User, create_store
from lascaux import Controller

from .forms import Register


class UserController(Controller):
    def register(self):
        self.save(self.render("register"))
        #self.save(Register("123").render())