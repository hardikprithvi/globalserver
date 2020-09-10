import requests
import json
import configparser
from check_licensing import decrypt_message,load_key

config = configparser.ConfigParser()
config.read('config_test.ini')
config['DEFAULT']['token nonitsm'] = decrypt_message(bytes(config['DEFAULT']['token nonitsm'],'utf-8'))

def raiseTicket(name,email,phno,description):
    header = {"Token":config["DEFAULT"]["token nonitsm"]}
    URL = config["DEFAULT"]["api link nonitsm"]+"RegisterComplain"
    print(URL)
    data = {
      "Id": 0,
      "ComplainNo": "AFS10012381",
      "ContactPerson": name,
      "ContactPersonEmail": email,
      "ContactPersonPhoneNumber": phno,
      "ProblemDescription": description,
      "SerialNo": "123",
      "ComplainStatusId": 1,
      "LocationMasterId": 1,
      "ComplainTypeId": 1,
      "ModelTypeId": 1,
      "ProblemTypeId": 1,
      "ProblemSubTypeId": 63,
      "PriorityId": 4,

    }

    r1 = requests.post(url = URL, headers = header, data = data)
    return r1.json()