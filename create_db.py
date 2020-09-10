from sqlalchemy import create_engine
import pandas as pd
import configparser
import time
from check_licensing import decrypt_message,load_key

config = configparser.ConfigParser()
config.read('config_test.ini')
config['DEFAULT']['sql password'] = decrypt_message(bytes(config['DEFAULT']['sql password'],'utf-8'))

# engine = create_engine("mysql+pymysql://"+config["DEFAULT"]["sql username"]+":"+config["DEFAULT"]["sql password"]+"@127.0.0.1:"+config["DEFAULT"]["sql port"]+"/"+config["DEFAULT"]["sql database name"])
# sql link manage = mysql+pymysql://dev:Dev@1234@@127.0.0.1/manage_engine?host=localhost
# sql link symphony = mysql+pymysql://dev:Dev@1234@@127.0.0.1/symphony?host=localhost


if(config['DEFAULT']['itsm tool name'].lower() == 'symphony'):
    
    engine = create_engine("mysql+pymysql://"+config["DEFAULT"]["sql username"]+":"+config["DEFAULT"]["sql password"]+"@"+config["DEFAULT"]["sql ip"]+":"+config["DEFAULT"]["sql port"]+"/symphony")
    
elif(config['DEFAULT']['itsm tool name'].lower() == 'manage engine'):
    
    engine = create_engine("mysql+pymysql://"+config["DEFAULT"]["sql username"]+":"+config["DEFAULT"]["sql password"]+"@"+config["DEFAULT"]["sql ip"]+":"+config["DEFAULT"]["sql port"]+"/manage_engine")
    
elif(config['DEFAULT']['itsm tool name'].lower() == 'non itsm'):
    
    engine = create_engine("mysql+pymysql://"+config["DEFAULT"]["sql username"]+":"+config["DEFAULT"]["sql password"]+"@"+config["DEFAULT"]["sql ip"]+":"+config["DEFAULT"]["sql port"]+"/non_itsm")
    
else:
    print("itsm tool name not specified in the config file")
    time.sleep(5)
    sys.exit(1)


def check_table():
    with engine.begin() as conn:
        print("where")
        conn.execute('''CREATE TABLE IF NOT EXISTS userdetails( Hostname VARCHAR(255),`IP_Address` VARCHAR(255),`MAC_ID` VARCHAR(255),
                                                                               `Serial_Number` VARCHAR(255),
                                                                                   `OS_Version` VARCHAR(255),
                                                                                   `Laptop_Desktop` VARCHAR(255),
                                                                                   `IN_SERVER` VARCHAR(255),
                                                                                   `OUT_SERVER` VARCHAR(255),
                                                                                   `Direct_Printers` VARCHAR(255),
                                                                                   `User_Name` VARCHAR(255),
                                                                                   `emailid` VARCHAR(255));''')
    
        conn.execute('''CREATE TABLE IF NOT EXISTS tickets (`Incident ID` VARCHAR(255),Description VARCHAR(255),`Private Log` VARCHAR(255),
                                                           Caller VARCHAR(255),
                                                           Tenant VARCHAR(255),
                                                           User_Mail VARCHAR(255),
                                                           Location VARCHAR(255),
                                                           Medium VARCHAR(255),
                                                           Source VARCHAR(255),
                                                           `Logged Time` VARCHAR(255),
                                                           Urgency VARCHAR(255),
                                                           Impact VARCHAR(255),
                                                           Priority VARCHAR(255),
                                                           `Work Group` VARCHAR(255),
                                                           `Assigned To` VARCHAR(255),
                                                           `Service Window` VARCHAR(255),
                                                           predicted_class_num VARCHAR(255),
                                                           Issue_Class VARCHAR(255),
                                                           Status VARCHAR(50),
                                                           Solution VARCHAR(50),
                                                           MAC_ID VARCHAR(50));''')

        conn.execute('''CREATE TABLE IF NOT EXISTS feedbacks( comment VARCHAR(255),Ticket VARCHAR(255),MAC_ID VARCHAR(255));''')
    
    return "table created"


def get_data():
    df = pd.read_sql('SELECT * FROM tickets', engine)
    return df

def getuser_Data():
    df = pd.read_sql('SELECT * FROM userdetails', engine)
    return df

def before_pred(df):
    df.to_sql(con=engine, name='tickets',if_exists = 'append',index=False)   
    return "updated"

def update(df):
    for i in range(0,len(df)):
        query = "update tickets set Solution='"+str(df['Solution'][i])+"', Status='"+str(df['Status'][i])+"' where `Incident ID` = '"+str(df['Incident ID'][i])+"';"
        print(query)
        with engine.begin() as conn:     # TRANSACTION
            conn.execute(query)
    return 'Updated'

def updatenew(tid):
    query = "update tickets set Status='Resolved' where `Incident ID` = '"+tid+"';"
    print(query)
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)
    return 'Updated'

def adduser_details(Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name):
    email = "as@gmail.com"
    query = "INSERT INTO userdetails VALUES ('"+Hostname+"','"+IP_Address+"','"+MAC_ID+"','"+Serial_Number+"','"+OS_Version+"','"+Laptop_Desktop+"','"+IN_SERVER+"','"+OUT_SERVER+"','"+Direct_Printers+"','"+User_Name+"','"+email+"')"
    with engine.begin() as conn:     # TRANSACTION
            conn.execute(query)

def adduser_update(Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name):
    email = "as@gmail.com"
    query = "update userdetails set OUT_SERVER='"+OUT_SERVER+"',IN_SERVER='"+IN_SERVER+"',Hostname='"+Hostname+"', IP_Address='"+IP_Address+"' , Serial_Number='"+Serial_Number+"' , OS_Version='"+OS_Version+"' , Laptop_Desktop='"+Laptop_Desktop+"', Direct_Printers='"+Direct_Printers+"' , User_Name='"+User_Name+"' , emailid='"+email+"' where MAC_ID = '"+MAC_ID+"';"
    print(query)
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)
    return 'Updated'

def fetchquery(query):
    df = pd.read_sql(query,engine)
    return df

def createnewuser(query):
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)
    return 'Created'

def feedback(text, macid, tid):
    query = "INSERT INTO feedbacks VALUES('"+text+"','"+macid+"','"+tid+"');"
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)
    return "feedback stored!"

def emaildb(text,macid):
    query = "update userdetails set emailid='"+text+"' where MAC_ID = '"+macid+"';"
    print(query)
    with engine.begin() as conn:     # TRANSACTION
        conn.execute(query)
    return "Email Updated"