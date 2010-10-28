import base64
import hashlib


def encrypt(String, Password):
    password = ""
    for character in Password:
        password += hashlib.sha1(character).hexdigest()
    password = hashlib.sha1(password).hexdigest()
    encrypted = ""
    for character in String:
        encrypted_character = ord(character)
        for c in password:
            encrypted_character = encrypted_character + ord(c)
        encrypted += str(encrypted_character)
    return base64.b64encode(str(encrypted))

def decrypt(String, Password):
    password = ""
    for character in Password:
        password += hashlib.sha1(character).hexdigest()
    password = hashlib.sha1(password).hexdigest()
    decrypted = ""
    elements = []
    s = base64.b64decode(String)
    for i in xrange(len(s)/4):
        elements.append(s[i*4:i*4+4])
    for element in elements:
        try:
            decrypted_character = int(element)
        except:
            return ""
        for c in password:
            decrypted_character -= ord(c)
        try:
            decrypted += chr(decrypted_character)
        except:
            pass
    return decrypted
