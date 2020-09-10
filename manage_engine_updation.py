import requests
import json
import config
import pandas as pd
import create_db
from check_licensing import decrypt_message,load_key

import configparser
config = configparser.ConfigParser()
config.read('config_test.ini')
config['DEFAULT']['token manage'] = decrypt_message(bytes(config['DEFAULT']['token manage'],'utf-8'))

def ticket_updation(df):
    for i in range(len(df)):
        # config.logger.info('Fetching ticket')
        inc_id = df.iloc[i]['Incident ID']
        data = {"input_data":json.dumps({
            "request": {
               "status": {
                    "name": "Resolved"
                },
                'status_change_comments': "Issue has been successfully resolved"
            }}) }
        URL= URL = config["DEFAULT"]["api link manage"] + str(inc_id)
        header = {"Authtoken": config["DEFAULT"]["token manage"]}
        r1 = requests.put(url = URL, verify= False, headers=header, data = data)
        # config.logger.info('Ticket status changed')
    return r1.json()

def updatetickets(ticket_id,status,solution):
    # config.logger.exception("In update ticket part")
    query = "select * from tickets where `Incident ID` = '"+ticket_id+"';"
    df=create_db.fetchquery(query)
    df.loc[df["Incident ID"]==ticket_id , 'Status'] = status
    df.loc[df["Incident ID"]==ticket_id , 'Solution'] = solution
    print(df)
    ret = create_db.update(df)
    # config.logger.exception('data updated in db')

    ticket_updation(df.loc[df.Status =="Resolved"]) 
    # config.logger.exception('ticket updated in itsm')


# s = ticket_updation(df)