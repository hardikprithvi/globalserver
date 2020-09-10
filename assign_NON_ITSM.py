import requests
import json
import config
import pandas as pd
import create_db
from check_licensing import decrypt_message,load_key

import configparser
config = configparser.ConfigParser()
config.read('config_test.ini')
config['DEFAULT']['token nonitsm'] = decrypt_message(bytes(config['DEFAULT']['token nonitsm'],'utf-8'))

def Assign_to(df):
    flag = True
    for i in range(len(df)):
        x = df.iloc[i]['Incident ID']
        header = {"Token": config["DEFAULT"]["token nonitsm"]}
        URL = config["DEFAULT"]["api link nonitsm"]+"ComplainAssignemt"
        data = {
            "Id": config["DEFAULT"]["id nonitsm"],
            "AssignmentId": 1,
            "ComplainId": int(x),
            "UserId": config["DEFAULT"]["userid nonitsm"],
            "ComplainPendingComments": "Ticket assigned to Technician",
            "ComplainCloseComments": "Not being able to resolve by Qfix",
            "Observation": "Not being able to resolve by Qfix",
            "ActionTaken": "Not being able to resolve by Qfix",
            "ComplainStatusId": 5,
            "ComplainClosedBy": "Aforesight",
            "ComplainClosureId": ""
        }
        r1 = requests.post(url=URL, headers=header, data=data)
        try:
            b = r1.json()
            print(b)
        except:
            return False
    return flag
def assigntickets(ticket_id):
    # config.logger.exception("In update ticket part")
    query = "select * from tickets where `Incident ID` = '"+str(ticket_id)+"';"
    df=create_db.fetchquery(query)
    df.loc[df["Incident ID"]==str(ticket_id) , 'Status'] = "Fail"
    df.loc[df["Incident ID"]==str(ticket_id) , 'Solution'] = "assigned to different technician"
    print(df)
    ret = create_db.update(df)
    # config.logger.exception('data updated in db')

    Assign_to(df.loc[df.Status =="Fail"]) 
    # config.logger.exception('ticket updated in itsm')
    