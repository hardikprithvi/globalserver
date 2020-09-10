import configparser
from getpass import getpass
from cryptography.fernet import Fernet
import time

def load_key():
    return open("secret.key", "rb").read()
def encrypt_message(message):
    key = load_key()
    encoded_message = message.encode()
    f = Fernet(key)
    encrypted_message = f.encrypt(encoded_message)
    return str(encrypted_message)[2:-1]

config = configparser.ConfigParser()
config.read('config_test.ini')

while(True):
    print("Password Menu")
    print('-'*10)
    print('Enter 1 to set the symphony password')
    print('Enter 2 to set the email sender password')
    print('Enter 3 to set the sql password')
    print('Enter 4 to set the non itsm token')
    print('Enter 5 to set the manage engine token')
    print('Enter 6 to set the software password')
    print('Enter any other key to exit')
    print('-' * 10)
    try:
        s = int(input())
    except:
        break
    if(s==1):
        s1 = getpass()
        config['DEFAULT']['login pass'] = encrypt_message(s1)
        with open('config_test.ini', 'w') as configfile:
            config.write(configfile)
        print('Symphony password updated!!')
        print('')
        time.sleep(2)
    elif(s==2):
        s1 = getpass()
        config['DEFAULT']['email send pass'] = encrypt_message(s1)
        with open('config_test.ini', 'w') as configfile:
            config.write(configfile)
        print('Email Sender password updated!!')
        print('')
        time.sleep(2)
    elif(s==3):
        s1 = getpass()
        config['DEFAULT']['sql password'] = encrypt_message(s1)
        with open('config_test.ini', 'w') as configfile:
            config.write(configfile)
        print('SQL Database password updated!!')
        print('')
        time.sleep(2)
    elif(s==4):
        print('Enter token: ',end='')
        s1 = input()
        config['DEFAULT']['token nonitsm'] = encrypt_message(s1)
        with open('config_test.ini', 'w') as configfile:
            config.write(configfile)
        print('NON ITSM token updated!!')
        print('')
        time.sleep(2)
    elif(s==5):
        print('Enter token: ', end='')
        s1 = input()
        config['DEFAULT']['token manage'] = encrypt_message(s1)
        with open('config_test.ini', 'w') as configfile:
            config.write(configfile)
        print('Manage Engine token updated!!')
        print('')
        time.sleep(2)
    elif (s == 6):
        s1 = getpass()
        config['DEFAULT']['software password'] = encrypt_message(s1)
        with open('config_test.ini', 'w') as configfile:
            config.write(configfile)
        print('Software password updated!!')
        print('')
        time.sleep(2)
    else:
        break





