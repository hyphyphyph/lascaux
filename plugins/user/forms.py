from petrified import Form
from petrified.widgets import *


class Register(Form):
    
    __order__ = ["username", "email", 
                 "password", "password_confirm", 
                 "register"]
    
    username = Text(required=True, title="Username", 
                    error_message="You have to enter a username.")
    email = Text(required=True, title="Email", 
                 error_message="You have to enter your email.")
    password = Password(required=True, title="Password", 
                        error_message="You have to enter a password.")
    password_confirm = Password(title="Confirm Password")
    register = Button(title="Register")