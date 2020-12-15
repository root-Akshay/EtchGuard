import secrets
import string

def generate_password():
    alphabet = string.ascii_letters + string.digits + string.punctuation
    password = ''.join(secrets.choice(alphabet) for i in range(15))
    """ print(password) """
    return password