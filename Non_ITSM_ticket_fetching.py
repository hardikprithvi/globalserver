import pandas as pd
import json
import requests
import predicting_part
import time
import configparser
from check_licensing import decrypt_message,load_key

config = configparser.ConfigParser()
config.read('config_test.ini')
config['DEFAULT']['token nonitsm'] = decrypt_message(bytes(config['DEFAULT']['token nonitsm'],'utf-8'))

# import create_db
def loginAndFetchTickets(macid):
    URL = config["DEFAULT"]["api link nonitsm"]+"ListOfComplains"
    header = {"Token": config["DEFAULT"]["token nonitsm"]}

    r = requests.get(url=URL, verify=False, headers=header)
    data = r.json()
    print(data)
    incd_id = []
    sptm = []
    prv_log = []
    soln = []
    cal = []
    ten = []
    loc = []
    med = []
    src = []
    log_tm = []
    urg = []
    imp = []
    pr = []
    wg = []
    at = []
    sw = []
    rc = []
    emails = []
    # Calculating number of tickets
    num_of_tickets = len(data)
    print(num_of_tickets)
    for row in data:
        try:
            print('Finding ticket attributes and storing it in a dataframe')
            # print(row['complain']['complainstatus']['ComplainStatus'])
            # This checks if the ticket is new
            if row['complain']['complainstatus']['ComplainStatus'] == 'New':
                # print(row['complain']['Id'])
                inc_id = row['complain']['Id']
                print(inc_id, "picked up")

                URL = "http://103.251.216.101/dat/Complain/ComplainAssignemt"
                data = {
                    "Id": 0,
                    "AssignmentId": 1,
                    "ComplainId": inc_id,
                    "UserId": config["DEFAULT"]["userid nonitsm"],
                    "ComplainPendingComments": "Picked up Aforesight BOT",
                    "ComplainCloseComments": "Picked up Aforesight BOT",
                    "Observation": "Observation",
                    "ActionTaken": "Solving by Aforesight Bot",
                    "ComplainStatusId": 3,
                    "ComplainClosedBy": "Aforesight",
                    "ComplainClosureId": ""
                }
                r1 = requests.post(url=URL, headers=header, data=data)
                print(r1.json())
                print("Changed to In Progress")
                print("Assigned to Aforesight")

                incd_id.append(inc_id)
                # This stores the symptoms and appends
                symptom = row['complain']['ProblemDescription']
                sptm.append(symptom)
                # This stores the private log
                private_logg = None
                prv_log.append(private_logg)
                # This stores the solution
                sol = None
                soln.append(sol)
                # Caller
                caller = row['complain']['ContactPerson']
                cal.append(caller)
                # Tenant
                tenant = None
                ten.append(tenant)
                # Email
                email = row['complain']['ContactPersonEmail']
                emails.append(email)
                # Location
                location = row['complain']['location']['LocationName']
                loc.append(location)
                # Medium
                medium = None
                med.append(medium)
                # Source
                source = None
                src.append(source)
                # Logged Time
                logg_time = row['complain']['ComplainRegDate']
                log_tm.append(logg_time)
                # Urgency 
                urgency = row['complain']['Priority']['Priority']
                urg.append(urgency)
                # Impact
                impact = row['complain']['Priority']['Priority']
                imp.append(impact)
                # Priority
                priority = row['complain']['Priority']['Priority']
                pr.append(priority)
                # Workgroup
                wrk_gp = row['complain']['location']['Office']
                wg.append(wrk_gp)
                # Assigned to
                assg_to = row['AssignTo']
                at.append(assg_to)
                # Service window
                serv_win = None
                sw.append(serv_win)
                # Resolution code
                resol_code = None
                rc.append(resol_code)
            else:
                continue
        except Exception as e:
            print('Error in storing attributes of a ticket ' + str(e))
    print('Storing values in a dataframe')
    df_dict = {'Incident ID': incd_id, 'Description': sptm, 'Private Log': prv_log, 'Caller': cal, 'Tenant': ten, \
               'User_Mail': emails, 'Location': loc, 'Medium': med, 'Source': src, 'Logged Time': log_tm,
               'Urgency': urg, 'Impact': imp, 'Priority': pr, \
               'Work Group': wg, 'Assigned To': at, 'Service Window': sw, 'MAC_ID':macid}  # ,'Resolution Code':rc,'Solution':soln,}
#     print(len(sptm), len(prv_log), len(cal), len(ten), len(emails), len(loc), len(med), len(src), len(log_tm), len(urg),
#           len(imp))
    df = pd.DataFrame(df_dict, index=None)
#     print('df unsorted is', df)
    # df.sort_values(by='Incident ID',inplace=True)
#     df.to_csv('Incidents_no_pred.csv')
    print('df sorted is\n', df)
    #     df.to_excel('Incidents.xlsx',sheet_name='All_Incidents')
    print('Calling the prediction script for ticket classification')
    df=predicting_part.predictionsOnEachTicket(df)
    df.sort_values(by='Incident ID',inplace=True)
    print("Done")
    return df, num_of_tickets


