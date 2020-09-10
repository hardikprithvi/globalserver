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

def assignto(df):
    for i in range(len(df)):
        t_id = df.iloc[i]['Incident ID']
        try:
            URL= config["DEFAULT"]["api link manage"]+str(t_id)+"/assign"
            header = {"Authtoken": config["DEFAULT"]["token manage"]}
            data = {"input_data":json.dumps({
                "request": {
                    "technician": {
                        "name": "Suraj Singh"
                    }
                }
            }) }
            r = requests.put(url = URL, verify= False, headers=header, data = data)
            if(r.json()['response_status']['status_code']!=2000):
                return "Wrong technician or API token expired"
            else:
                return "Ticket succesfully assigned to " + str(tech_name)
        except:
            return "Some error occured"
def assigntickets(ticket_id):
    # config.logger.exception("In update ticket part")
    query = "select * from tickets where `Incident ID` = '"+str(ticket_id)+"';"
    df=create_db.fetchquery(query)
    df.loc[df["Incident ID"]==str(ticket_id) , 'Status'] = "Fail"
    df.loc[df["Incident ID"]==str(ticket_id) , 'Solution'] = "assigned to different technician"
    print(df)
    ret = create_db.update(df)
    # config.logger.exception('data updated in db')

    assignto(df.loc[df.Status =="Fail"]) 
    # config.logger.exception('ticket updated in itsm')
    
# assigntickets(10)