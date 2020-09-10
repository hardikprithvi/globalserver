from cryptography.fernet import Fernet
import getmac
from datetime import datetime


def load_key():
    return open("secret.key", "rb").read()
def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return encrypted_message
print("\nEnter License key to be Encrypted : ")

s = input()
print("\n\nEncrypted Key : \n\n")
print(str(encrypt_message(s))[2:-1])