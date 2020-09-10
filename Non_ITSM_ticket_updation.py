import requests
import json
import config
import create_db
import configparser
from check_licensing import decrypt_message,load_key

config = configparser.ConfigParser()
config.read('config_test.ini')
config['DEFAULT']['token nonitsm'] = decrypt_message(bytes(config['DEFAULT']['token nonitsm'],'utf-8'))

def UpdateTicket(df):
    flag=True
    for i in range(len(df)):
        x = df.iloc[i]['Incident ID']
        header = {"Token":config["DEFAULT"]["token nonitsm"]}
        URL = config["DEFAULT"]["api link nonitsm"]+"ComplainAssignemt"
        data = {
          "Id": config["DEFAULT"]["id nonitsm"],
          "AssignmentId": 1,
          "ComplainId": int(x),
          "UserId": config["DEFAULT"]["userid nonitsm"],
          "ComplainPendingComments": "Resolved By Aforesight",
          "ComplainCloseComments": "Resolved By Aforesight",
          "Observation": df['Status'],
          "ActionTaken": df["Solution"],
          "ComplainStatusId": 6,
          "ComplainClosedBy": "Aforesight",
          "ComplainClosureId": ""
        }
        r1 = requests.post(url = URL, headers = header, data = data)
        try:
            b = r1.json()
        except:
            return False
    return flag

def updatetickets(ticket_id,status,solution):
    config.logger.exception("In update ticket part")
    query = "select * from tickets where `Incident ID` = '"+ticket_id+"';"
    df=create_db.fetchquery(query)
    df.loc[df["Incident ID"]==ticket_id , 'Status'] = status
    df.loc[df["Incident ID"]==ticket_id , 'Solution'] = solution
    print(df)
    ret = create_db.update(df)
    config.logger.exception('data updated in db')

    UpdateTicket(df.loc[df.Status =="Resolved"]) 
    config.logger.exception('ticket updated in itsm')
