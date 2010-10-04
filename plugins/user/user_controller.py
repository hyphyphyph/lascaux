import uuid
import hashlib
import time

from lascaux.model import User
from lascaux import Controller, config

from .user_forms import Register


class UserController(Controller):
    def register(self):
        form = Register(self.route(self, "register"))
        if self.request.POST:
            form.ingest(self.POST)
            if self.db.find(User, username=form.username().value).count():
                form.username.error = True
                form.username.error_message = "That username is already in use."
            if form.password().value != form.password_confirm().value:
                form.password.error = True
                form.password.error_message = "Your passwords don't match."
            if form.validates():
                user = User(uuid.uuid1().hex.decode())
                user.username = form.username().value
                user.email = form.email().value
                user.password = hashlib.sha1(
                    config.sap(form.password().value)).hexdigest().decode()
                user.created = int(time.time())
                self.db.add(user)
                self.db.flush()
                self.save(self.render("register_success", {
                    "username": user.username,
                    "email": user.email
                }))
                return True
            else:
                self.save(form.render(self.render("register_form")))
            return True
        self.save(form.render(self.render("register_form")))