from petrified import Form
from petrified.widgets import *


class Register(Form):
    
    __order__ = ["username", "email", 
                 "password", "password_confirm", 
                 "register"]
    
    username = Text(required=True, title="Username")
    email = Text(required=True, title="Email")
    password = Password(required=True, title="Password")
    password_confirm = Password(required=True, title="Confirm Password")
    register = Button(title="Register")