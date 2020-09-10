from flask import Flask, request, render_template, jsonify
import manage_engine_ticket_raising
import predict_nonitsm
import predict_symphony
import predict_manage
import pandas as pd
import create_db
import mail_send
import manage_engine_updation
import assign1
import configparser
from check_licensing import checklicense,decrypt_message,load_key
import sys
import time
import json
import createticket
import updateticketstatus
import generate_mail
import assignticket
import Non_ITSM_ticket_raising
import Non_ITSM_ticket_updation
import assign_NON_ITSM
import pem
config = configparser.ConfigParser()
config.read('config_test.ini')

try:
    key = pem.parse_file("software_afs.pem")
except :
    key = [""]


def run_manage_engine():
        
    
    # server = smtplib.SMTP('smtp.gmail.com:587')
    
    app = Flask(__name__)
    
    @app.route('/synclogs/<macid>', methods = ['GET','POST'])
    def synclogs(macid):
        print(macid)
        logs_new = request.data
        logs_new = json.loads(logs_new)
        logs_new = logs_new['logs_new']
        with open('logs/'+str(macid),'a') as file:
            file.write(logs_new)
        return 'synced'
    
    # route to store fedback in the database
    @app.route('/feedback/<text>/<macid>/<tid>', methods = ['GET','POST'])
    def feedback(text,macid,tid):
        print(text,macid,tid)
        ok = create_db.feedback(text,macid,tid)
        return ok
    
    @app.route('/emailadd/<em>/<macid>',methods = ['GET','POST'])
    def emailadd(em,macid):
        print(em,macid)
        ret = create_db.emaildb(em,macid)
        
        return ret
    
    @app.route('/newt/<subject>/<description>/<macid>', methods = ['GET','POST'])
    def newt(subject, description, macid):
        print(subject, description, macid)
        r_json = manage_engine_ticket_raising.ticket_raising(subject, description, config["DEFAULT"]["name manage"], config["DEFAULT"]["id manage"])
    #     print(r_json)
        t_id = r_json['request']['id']
    #     t_id = "456"
        print(t_id)
        predict_manage.predict(macid)
        query = "select emailid from userdetails where MAC_ID = '"+macid+"';"
        df = create_db.fetchquery(query)
        email = df.iloc[0]["emailid"]
        mail_send.raiseticket(str(email),'issue',t_id)
        return str(t_id)
    
    @app.route('/inoutserver/<macid>')
    def inoutserver(macid):
        df = create_db.getuser_Data()
        df = df.loc[df['MAC_ID']==macid]
        print(df)
        ins = df['IN_SERVER'].values[0]
        outs = df['OUT_SERVER'].values[0]
        print(ins,outs)
        data = {
            'inserver':str(ins),
            'outserver':str(outs)
        }
        return jsonify({'inserver':str(ins),'outserver':str(outs)})
    
    @app.route('/configdata', methods = ['GET','POST'])
    def configdata():
        inserver = config["DEFAULT"]["incoming server"]
        outserver = config["DEFAULT"]["outgoing server"]
        it_help = config["DEFAULT"]["it helpdesk"]
        policy_url = config["DEFAULT"]["it policy url"]
        myHostname = config["DEFAULT"]["software_hostname"]
        myUsername = config["DEFAULT"]["software_username"]
        pem_file = str(key[0])
        if len(config["DEFAULT"]["software_password"]) != 0:
            software_password = decrypt_message(bytes(config["DEFAULT"]["software_password"],'utf-8'))
        else:
            software_password = config["DEFAULT"]["software_password"]
        upload_link = config["DEFAULT"]["software upload link"]
        smtp_auth = config["DEFAULT"]["smtp_auth"]
        incoming_server_port  = config["DEFAULT"]["incoming_server_port"]
        outgoing_server_port = config["DEFAULT"]["outgoing_server_port"]
        type_of_encrypted_connection = config["DEFAULT"]["type_of_encrypted_connection"]
        requires_SSL_connection = config["DEFAULT"]["requires_SSL_connection"]
        return jsonify({'inserver':str(inserver),'outserver':str(outserver),'it_help':str(it_help),'policy_url':str(policy_url),'myhostname':str(myHostname),'myusername':str(myUsername),'pem_file':str(pem_file),'software_password':str(software_password),'software upload link':str(upload_link),'smtp_auth':str(smtp_auth),'incoming_server_port':str(incoming_server_port),'outgoing_server_port':outgoing_server_port,'type_of_encrypted_connection':type_of_encrypted_connection,'requires_SSL_connection':requires_SSL_connection})
    
    @app.route('/userdetails/<key>/<Hostname>/<IP_Address>/<MAC_ID>/<Serial_Number>/<OS_Version>/<Laptop_Desktop>/<IN_SERVER>/<OUT_SERVER>/<Direct_Printers>/<User_Name>', methods=['GET', 'POST'])
    def userdetail(key,Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name):
        if key == 'old':
            print(Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name)
            df = create_db.getuser_Data()
            if len(df.loc[df["MAC_ID"] == MAC_ID])>0:
                create_db.adduser_update(Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, str(IN_SERVER), str(OUT_SERVER), Direct_Printers, User_Name)
            else:
                create_db.adduser_details(Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name)
            return "done"
        elif key == 'new':
            query = "insert into userdetails values('1','1','"+str(MAC_ID)+"','1','1','1','"+str(IN_SERVER)+"','"+str(OUT_SERVER)+"','1','1','sx@gmail.com');"
            res = create_db.createnewuser(query)
            return 'done'
    
    @app.route('/oldt/<tid>', methods = ['GET', 'POST'])
    def oldt(tid):
        query = "select * from tickets where `Incident ID` = '"+str(tid)+"';"
        df = create_db.fetchquery(query)
        text = 'You had '+str(df.loc[df["Incident ID"] == str(tid)].Description.values[0])+' issue and status is '+str(df.loc[df["Incident ID"] == str(tid)].Status.values[0])
        return text
    
    @app.route('/upt/<tid>/<macid>', methods = ['GET','POST'])
    def upt(tid,macid):
        outp = create_db.updatenew(tid)
    #     df = create_db.get_data()
        query = "select * from tickets where `Incident ID` ='"+str(tid)+"';"
        print(query)
        df = create_db.fetchquery(query)
        print(df["Issue_Class"][0])
        manage_engine_updation.updatetickets(str(tid),'Resolved','Issue has been successfully resolved')
        query = "select emailid from userdetails where MAC_ID = '"+macid+"';"
        df2 = create_db.fetchquery(query)
        email = df2.iloc[0]["emailid"]
        mail_send.updateticket(email,df["Issue_Class"][0],"Resolved",str(tid))
        if outp == 'Updated':
            return 'Ticket resolved successfully'
        else:
            return 'Some Error While Resolving Issue'
        return 'Ticket resolved successfully'
    
    @app.route('/assign/<tid>/<macid>', methods = ['GET','POST'])
    def assign(tid,macid):
        outp = create_db.updatenew(tid)
    #     df = create_db.get_data()
        query = "select * from tickets where `Incident ID` ='"+str(tid)+"';"
        print(query)
        df = create_db.fetchquery(query)
        print(df["Issue_Class"][0])
        assign1.assigntickets(tid)
        query = "select emailid from userdetails where MAC_ID = '"+macid+"';"
        df2 = create_db.fetchquery(query)
        email = df2.iloc[0]["emailid"]
        mail_send.updateticket(email,df["Issue_Class"][0],"Assigned to expert.",str(tid))    
        if outp == 'Updated':
            return 'Assigned to Expert.'
        else:
            return 'Some Error While Resolving Issue'
        return 'Assigned to Expert.'
    
    @app.route('/know/<macid>',methods = ['GET','POST'])
    def know(macid):
        query = "select * from tickets where MAC_ID = '"+macid+"';"
        df = create_db.fetchquery(query)
        df = df.to_json()
        return df
    
    @app.route('/getalluniqueid', methods = ['GET','POST'])
    def getall():
        query = 'select MAC_ID from userdetails'
        df = create_db.fetchquery(query)
        df = df.to_json()
        return df
    if __name__ == '__main__':
        ret = create_db.check_table()
        print(ret)
        app.run(host = '0.0.0.0', port = 7006,ssl_context="adhoc")


#################################################################

def run_NON_ISTM():
    
    
    app = Flask(__name__)
    
    @app.route('/synclogs/<macid>', methods = ['GET','POST'])
    def synclogs(macid):
        print(macid)
        logs_new = request.data
        logs_new = json.loads(logs_new)
        logs_new = logs_new['logs_new']
        with open('logs/'+str(macid),'a') as file:
            file.write(logs_new)
        return 'synced'
    # route to store fedback in the database
    @app.route('/feedback/<text>/<macid>/<tid>', methods = ['GET','POST'])
    def feedback(text,macid,tid):
        print(text,macid,tid)
        ok = create_db.feedback(text,macid,tid)
        return ok
    
    @app.route('/emailadd/<em>/<macid>',methods = ['GET','POST'])
    def emailadd(em,macid):
        print(em,macid)
        ret = create_db.emaildb(em,macid)
        return ret
    @app.route('/newt/<subject>/<description>/<macid>', methods = ['GET','POST'])
    def newt(subject, description, macid):
        print(subject, description, macid)
        query = "select emailid from userdetails where MAC_ID = '"+macid+"';"
        df = create_db.fetchquery(query)
        email = df.iloc[0]["emailid"]
        r_json = Non_ITSM_ticket_raising.raiseTicket( config["DEFAULT"]["name nonitsm"],email, config["DEFAULT"]["number nonitsm"],description)
        print(r_json)
        t_id = r_json['Id']
    #     t_id = "456"
        print(t_id)
        predict_nonitsm.predict(macid)
        mail_send.raiseticket(str(email),'issue',str(t_id))
        return str(t_id)
    
    @app.route('/inoutserver/<macid>')
    def inoutserver(macid):
        df = create_db.getuser_Data()
        df = df.loc[df['MAC_ID']==macid]
        print(df)
        ins = df['IN_SERVER'].values[0]
        outs = df['OUT_SERVER'].values[0]
        print(ins,outs)
        data = {
            'inserver':str(ins),
            'outserver':str(outs)
        }
        return jsonify({'inserver':str(ins),'outserver':str(outs)})
    
    @app.route('/configdata', methods = ['GET','POST'])
    def configdata():
        inserver = config["DEFAULT"]["incoming server"]
        outserver = config["DEFAULT"]["outgoing server"]
        it_help = config["DEFAULT"]["it helpdesk"]
        policy_url = config["DEFAULT"]["it policy url"]
        myHostname = config["DEFAULT"]["software_hostname"]
        myUsername = config["DEFAULT"]["software_username"]
        pem_file = str(key[0])
        if len(config["DEFAULT"]["software_password"]) != 0:
            software_password = decrypt_message(bytes(config["DEFAULT"]["software_password"],'utf-8'))
        else:
            software_password = config["DEFAULT"]["software_password"]
        upload_link = config["DEFAULT"]["software upload link"]
        smtp_auth = config["DEFAULT"]["smtp_auth"]
        incoming_server_port  = config["DEFAULT"]["incoming_server_port"]
        outgoing_server_port = config["DEFAULT"]["outgoing_server_port"]
        type_of_encrypted_connection = config["DEFAULT"]["type_of_encrypted_connection"]
        requires_SSL_connection = config["DEFAULT"]["requires_SSL_connection"]
        return jsonify({'inserver':str(inserver),'outserver':str(outserver),'it_help':str(it_help),'policy_url':str(policy_url),'myhostname':str(myHostname),'myusername':str(myUsername),'pem_file':str(pem_file),'software_password':str(software_password),'software upload link':str(upload_link),'smtp_auth':str(smtp_auth),'incoming_server_port':str(incoming_server_port),'outgoing_server_port':outgoing_server_port,'type_of_encrypted_connection':type_of_encrypted_connection,'requires_SSL_connection':requires_SSL_connection})
    
    @app.route('/userdetails/<key>/<Hostname>/<IP_Address>/<MAC_ID>/<Serial_Number>/<OS_Version>/<Laptop_Desktop>/<IN_SERVER>/<OUT_SERVER>/<Direct_Printers>/<User_Name>', methods=['GET', 'POST'])
    def userdetail(key,Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name):
        if key == 'old':
            print(Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name)
            df = create_db.getuser_Data()
            if len(df.loc[df["MAC_ID"] == MAC_ID])>0:
                create_db.adduser_update(Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name)
            else:
                create_db.adduser_details(Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name)
            return "done"
        elif key == 'new':
            query = "insert into userdetails values('1','1','"+str(MAC_ID)+"','1','1','1','"+str(IN_SERVER)+"','"+str(OUT_SERVER)+"','1','1','sx@gmail.com');"
            res = create_db.createnewuser(query)
            return 'done'
    
    @app.route('/oldt/<tid>', methods = ['GET', 'POST'])
    def oldt(tid):
        query = "select * from tickets where `Incident ID` = '"+str(tid)+"';"
        df = create_db.fetchquery(query)
        text = 'You had '+str(df.loc[df["Incident ID"] == str(tid)].Description.values[0])+' issue and status is '+str(df.loc[df["Incident ID"] == str(tid)].Status.values[0])
        return text
    
    @app.route('/upt/<tid>/<macid>', methods = ['GET','POST'])
    def upt(tid,macid):
        outp = create_db.updatenew(tid)
    #     df = create_db.get_data()
        query = "select * from tickets where `Incident ID` ='"+str(tid)+"';"
        print(query)
        df = create_db.fetchquery(query)
        print(df["Issue_Class"][0])
        Non_ITSM_ticket_updation.updatetickets(str(tid),'Resolved','Issue has been successfully resolved')
        query = "select emailid from userdetails where MAC_ID = '"+macid+"';"
        df2 = create_db.fetchquery(query)
        email = df2.iloc[0]["emailid"]
        mail_send.updateticket(email,df["Issue_Class"][0],"Resolved",str(tid))
        if outp == 'Updated':
            return 'Ticket resolved successfully'
        else:
            return 'Some Error While Resolving Issue'
        return 'Ticket resolved successfully'
    
    @app.route('/assign/<tid>/<macid>', methods = ['GET','POST'])
    def assign(tid,macid):
        outp = create_db.updatenew(tid)
    #     df = create_db.get_data()
        query = "select * from tickets where `Incident ID` ='"+str(tid)+"';"
        print(query)
        df = create_db.fetchquery(query)
        print(df["Issue_Class"][0])
        assign_NON_ITSM.assigntickets(tid)
        query = "select emailid from userdetails where MAC_ID = '"+macid+"';"
        df2 = create_db.fetchquery(query)
        email = df2.iloc[0]["emailid"]
        mail_send.updateticket(email,df["Issue_Class"][0],"Assigned to expert",str(tid))   
        if outp == 'Updated':
            return 'Assigned to Expert.'
        else:
            return 'Some Error While Resolving Issue'
        return 'Assigned to Expert.'
    
    @app.route('/know/<macid>',methods = ['GET','POST'])
    def know(macid):
        query = "select * from tickets where MAC_ID = '"+macid+"';"
        df = create_db.fetchquery(query)
        df = df.to_json()
        return df
    
    @app.route('/getalluniqueid', methods = ['GET','POST'])
    def getall():
        query = 'select MAC_ID from userdetails'
        df = create_db.fetchquery(query)
        df = df.to_json()
        return df
    if __name__ == '__main__':
        ret = create_db.check_table()
        print(ret)
        app.run(host = '0.0.0.0', port = 7006,ssl_context="adhoc")

#####################################################################################

def run_symphony():
    
    app = Flask(__name__)
    
    @app.route('/synclogs/<macid>', methods = ['GET','POST'])
    def synclogs(macid):
        print(macid)
        logs_new = request.data
        logs_new = json.loads(logs_new)
        logs_new = logs_new['logs_new']
        with open('logs/'+str(macid),'a') as file:
            file.write(logs_new)
        return 'synced'
    # route to store fedback in the database
    @app.route('/feedback/<text>/<macid>/<tid>', methods = ['GET','POST'])
    def feedback(text,macid,tid):
        print(text,macid,tid)
        ok = create_db.feedback(text,macid,tid)
        return ok
    
    @app.route('/emailadd/<em>/<macid>',methods = ['GET','POST'])
    def emailadd(em,macid):
        print(em,macid)
        ret = create_db.emaildb(em,macid)
        return ret
    
    @app.route('/newt/<symptom>/<description>/<macid>', methods = ['GET','POST'])
    def newt(symptom,description,macid):
        print(symptom,description)
        query = "select emailid from userdetails where MAC_ID = '"+macid+"';"
        df = create_db.fetchquery(query)
        email = df.iloc[0]["emailid"]
        t_id = createticket.loginAndCreateTickets(symptom,description)
    #     t_id = "456"
        print(t_id)
        predict_symphony.predict(macid)
        generate_mail.raiseticket(str(email),'issue',t_id)
        return str(t_id)
    
    @app.route('/inoutserver/<macid>')
    def inoutserver(macid):
        print(macid)
        df = create_db.fetchquery('select * from userdetails where MAC_ID = "'+str(macid)+'";')
        print(df)
        ins = df['IN_SERVER'][0]
        print(ins)
        outs = df['OUT_SERVER'][0]
        print(outs)
        data = {
            'inserver':str(ins),
            'outserver':str(outs)
        }
        return jsonify({'inserver':str(ins),'outserver':str(outs)})
    
    @app.route('/configdata', methods = ['GET','POST'])
    def configdata():
        inserver = config["DEFAULT"]["incoming server"]
        outserver = config["DEFAULT"]["outgoing server"]
        it_help = config["DEFAULT"]["it helpdesk"]
        policy_url = config["DEFAULT"]["it policy url"]
        myHostname = config["DEFAULT"]["software_hostname"]
        myUsername = config["DEFAULT"]["software_username"]
        pem_file = str(key[0])
        if len(config["DEFAULT"]["software_password"]) != 0:
            software_password = decrypt_message(bytes(config["DEFAULT"]["software_password"],'utf-8'))
        else:
            software_password = config["DEFAULT"]["software_password"]
        upload_link = config["DEFAULT"]["software upload link"]
        smtp_auth = config["DEFAULT"]["smtp_auth"]
        incoming_server_port  = config["DEFAULT"]["incoming_server_port"]
        outgoing_server_port = config["DEFAULT"]["outgoing_server_port"]
        type_of_encrypted_connection = config["DEFAULT"]["type_of_encrypted_connection"]
        requires_SSL_connection = config["DEFAULT"]["requires_SSL_connection"]
        return jsonify({'inserver':str(inserver),'outserver':str(outserver),'it_help':str(it_help),'policy_url':str(policy_url),'myhostname':str(myHostname),'myusername':str(myUsername),'pem_file':str(pem_file),'software_password':str(software_password),'software upload link':str(upload_link),'smtp_auth':str(smtp_auth),'incoming_server_port':str(incoming_server_port),'outgoing_server_port':outgoing_server_port,'type_of_encrypted_connection':type_of_encrypted_connection,'requires_SSL_connection':requires_SSL_connection})
    
    @app.route('/userdetails/<key>/<Hostname>/<IP_Address>/<MAC_ID>/<Serial_Number>/<OS_Version>/<Laptop_Desktop>/<IN_SERVER>/<OUT_SERVER>/<Direct_Printers>/<User_Name>', methods=['GET', 'POST'])
    def userdetail(key,Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name):
        if key == 'old':
            print(Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name)
            df = create_db.getuser_Data()
            if len(df.loc[df["MAC_ID"] == MAC_ID])>0:
                create_db.adduser_update(Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name)
            else:
                create_db.adduser_details(Hostname, IP_Address, MAC_ID, Serial_Number, OS_Version, Laptop_Desktop, IN_SERVER, OUT_SERVER, Direct_Printers, User_Name)
            return "done"
        elif key == 'new':
            query = "insert into userdetails values('1','1','"+str(MAC_ID)+"','1','1','1','"+str(IN_SERVER)+"','"+str(OUT_SERVER)+"','1','1','as@gmail.com');"
            res = create_db.createnewuser(query)
            return 'done'
    
    @app.route('/oldt/<tid>', methods = ['GET', 'POST'])
    def oldt(tid):
        query = "select * from tickets where `Incident ID` = '"+str(tid)+"';"
        df = create_db.fetchquery(query)
        text = 'You had '+str(df.loc[df["Incident ID"] == str(tid)].Description.values[0])+' issue and status is '+str(df.loc[df["Incident ID"] == str(tid)].Status.values[0])
        return text
    
    @app.route('/upt/<tid>/<macid>', methods = ['GET','POST'])
    def upt(tid,macid):
        outp = create_db.updatenew(tid)
    #     df = create_db.get_data()
        query = "select * from tickets where `Incident ID` ='"+str(tid)+"';"
        print(query)
        df = create_db.fetchquery(query)
        print(df["Issue_Class"][0])
        updateticketstatus.updateTicket_2(str(tid),'Resolved','Issue has been successfully resolved')
        query = "select emailid from userdetails where MAC_ID = '"+macid+"';"
        df2 = create_db.fetchquery(query)
        email = df2.iloc[0]["emailid"]
        generate_mail.updateticket(email,df["Issue_Class"][0],"Resolved",str(tid))
        if outp == 'Updated':
            return 'Ticket resolved successfully'
        else:
            return 'Some Error While Resolving Issue'
        return 'Ticket resolved successfully'
    
    @app.route('/assign/<tid>/<macid>', methods = ['GET','POST'])
    def assign(tid,macid):
        outp = create_db.updatenew(tid)
    #     df = create_db.get_data()
        query = "select * from tickets where `Incident ID` ='"+str(tid)+"';"
        print(query)
        df = create_db.fetchquery(query)
        print(df["Issue_Class"][0])
        assignticket.Ticketassign_2(str(tid))
        query = "select emailid from userdetails where MAC_ID = '"+macid+"';"
        df2 = create_db.fetchquery(query)
        email = df2.iloc[0]["emailid"]
        generate_mail.updateticket(email,df["Issue_Class"][0],"assigned to expert",str(tid))
        if outp == 'Updated':
            return 'Assigned to Expert.'
        else:
            return 'Some Error While Resolving Issue'
        return 'Assigned to Expert.'
    
    @app.route('/know/<macid>',methods = ['GET','POST'])
    def know(macid):
        query = "select * from tickets where MAC_ID = '"+macid+"';"
        df = create_db.fetchquery(query)
        df = df.to_json()
        return df
    
    @app.route('/getalluniqueid', methods = ['GET','POST'])
    def getall():
        query = 'select MAC_ID from userdetails'
        df = create_db.fetchquery(query)
        df = df.to_json()
        return df
    
    if __name__ == '__main__':
        ret = create_db.check_table()
        print(ret)
        app.run(host = '0.0.0.0', port = 7006,ssl_context="adhoc")


status, msg = checklicense()
if status == 0:
    print("\nKey = "+ msg + "\nPlease mail this key to Aforesight for verification.")
    time.sleep(60)
    
elif status == 1:
    if(config['DEFAULT']['itsm tool name'].lower() == 'symphony'):
        run_symphony()
    elif(config['DEFAULT']['itsm tool name'].lower() == 'manage engine'):
        run_manage_engine()
    elif(config['DEFAULT']['itsm tool name'].lower() == 'non itsm'):
        run_NON_ISTM()
    else:
        print("ITSM Tool Not Supported")
        time.sleep(5)
        sys.exit(1)

else:
    print("Key Not Correct. Contact Aforeight.")
    time.sleep(5)
    sys.exit(1)