import getmac
from datetime import datetime,date
import configparser
from cryptography.fernet import Fernet

def load_key():
    return open("secret.key", "rb").read()

def decrypt_message(encrypted_message):
    key = load_key()
    f = Fernet(key)
    decrypted_message = f.decrypt(encrypted_message)
    return (decrypted_message.decode())

def verify_license(s):
    
    try:
        license_key = (decrypt_message(bytes(s,'utf-8')))
        mac_id, license_date = license_key.split('$')
        
        mac_id = list(mac_id)
        for i in range(1,len(mac_id)+1):
            if(i%3 == 0):
                mac_id[i-1] = ':'
        mac_id = ''.join(mac_id)
        
        license_date = date(int(license_date[0:4]),int(license_date[5:7]),int(license_date[8:10]))
        
        chk_days = (datetime.date(datetime.now()) - license_date).days
        
    except :
        return (2,"Wrong License Key!! Please contact Aforesight")
    
    if((chk_days)<=15 and mac_id == getmac.get_mac_address()):
        return (1,"OK License Verified!!")
    else:
        return (2,"Wrong License Key!! Please contact Aforesight")

def new_license():
    license_key = str(getmac.get_mac_address()) + '$'+str(datetime.date(datetime.now()))
    license_key = list(license_key)
    for i in range(len(license_key)):
        if(license_key[i]==':'):
            license_key[i] = '7'
        elif(license_key[i]=='-'):
            license_key[i]='9'
    license_key = ''.join(license_key)

    return license_key

def checklicense():
    config = configparser.ConfigParser()
    config.read('config_test.ini')
    check_key = config["DEFAULT"]["license key"] 
    
    if check_key == "":
        key = new_license()
        return (0,key)
    else:
        return verify_license(str(check_key))