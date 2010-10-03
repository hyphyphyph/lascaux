from lascaux.model import User, create_store
from lascaux import Controller


class UserController(Controller):
    def register(self):
        store = create_store()
        user = User()
        user.uuid = u"123"
        user.username = u"ABDEKHKHFDA"
        store.add(user)
        store.flush()