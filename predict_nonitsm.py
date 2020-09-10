import time
import smtplib
import config
from datetime import datetime, timedelta
import pandas as pd
import dateutil.parser
import json
import Non_ITSM_ticket_fetching
import predicting_part
import create_db
def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'w+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

		
		

def predict(macid):  # pass paramter macid
    global df
    
    config.logger.info('Logging in ITSM tool for fetching tickets')
    df,num_of_tickets=Non_ITSM_ticket_fetching.loginAndFetchTickets(macid)
    class_mapping={0:'DiskCLeanup',1:'Email',2:'Others',3:'Password',4:'Printer',5:'SoftwareInstall'}
    df['Issue_Class']=df['predicted_class_num'].map(class_mapping)
    df3=df.copy()
    df3.drop(['predicted_class_num'],axis=1,inplace=True)
    df['Status']="In-Progress"    # saving values for testing
    df['Solution']=None
    print(create_db.before_pred(df))