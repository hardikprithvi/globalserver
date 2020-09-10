# from flask import Flask,request,render_template
from selenium.webdriver.common.keys import Keys
from csv import writer
import time
import smtplib
import config
import pandas as pd
import dateutil.parser
import json
import manage_engine_ticket_fetching
import create_db


def append_list_as_row(file_name, list_of_elem):
    with open(file_name, 'w+', newline='') as write_obj:
        # Create a writer object from csv module
        csv_writer = writer(write_obj)
        # Add contents of list as last row in the csv file
        csv_writer.writerow(list_of_elem)

		
		

def predict(macid):
    global df
        
    config.logger.info('Logging in ITSM tool for fetching tickets')
    df,num_of_tickets = manage_engine_ticket_fetching.loginAndFetchTickets(macid)
    
    class_mapping={0:'DiskCLeanup',1:'Email',2:'Others',3:'Password',4:'Printer',5:'SoftwareInstall'}
    print(df.columns)
    df['Issue_Class']=df['predicted_class_num'].map(class_mapping)
#     df.to_excel('All_Incidents.xlsx',sheet_name='Incidents',index=False)
    df3=df.copy()
    df3.drop(['predicted_class_num'],axis=1,inplace=True)
    df['Status']="In-Progress"    # saving values for testing
    df['Solution']=None
#     df.to_csv('Incidents.csv')
#     print(df.dtypes)
#     print(df.columns)
    print(create_db.before_pred(df))
    