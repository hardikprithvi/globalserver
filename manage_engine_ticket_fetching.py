import pandas as pd
import predicting_part
import config
import requests
import json
import create_db
from check_licensing import decrypt_message,load_key

import configparser
config = configparser.ConfigParser()
config.read('config_test.ini')
config['DEFAULT']['token manage'] = decrypt_message(bytes(config['DEFAULT']['token manage'],'utf-8'))

def loginAndFetchTickets(macid):
    # Fetching all requests currently in the ITSM tool
    # config.logger.info('Fetching all requests currently in the ITSM tool')
    URL =  config["DEFAULT"]["api link manage"]
    header = {"Authtoken": config["DEFAULT"]["token manage"]}
    data = {"input_data": json.dumps({"list_info": {
        "search_fields": {
            "status": "New"
        },
        "filter_by": {
            "status": "New"
        }
    }})}
    # GET type request to fetch all tickets with parameters as auth key and data
    # config.logger.info('GET type request to fetch all tickets with parameters as auth key and data')
    r = requests.get(url=URL, verify=False, headers=header, data=data)

    # config.logger.info('Converting the response to a readable json')
    data = r.json() # Converting the response to a readable json

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
    # config.logger.info('Calculating number of tickets')
    num_of_tickets = data['list_info']['row_count']
    print(num_of_tickets)

    for row in data['requests']:
        try:
            print('Finding ticket attributes and storing it in a dataframe')
            # This checks if the ticket is new
            # config.logger.info('Checking if the ticket is new')

            if row['status']['name'] == 'Open':
                inc_id = row['id']
                print(inc_id, "picked up")


                data = {"input_data": json.dumps({
                    "request": {
                        "status": {
                            "name": "In Progress"
                        },
                        'status_change_comments': "Picked up by aforesight"
                    }})}
                URL = config["DEFAULT"]["api link manage"] + str(inc_id)

                # PUT request to update status to In Progress
                # config.logger.info('updating status to In Progress')

                r1 = requests.put(url=URL, verify=False, headers=header, data=data)
                #print(r1.json())
                # config.logger.info("Changed to In Progress")

                URL = config["DEFAULT"]["api link manage"] + str(inc_id) + "/pickup"
                # PUT request for picking up ticket by AFORESIGHT
                # config.logger.info('picking up ticket by AFORESIGHT')
                r2 = requests.put(url=URL, verify=False, headers=header)
                print(r2.json())

                # config.logger.info("Assigned to Aforesight")

                incd_id.append(inc_id)

                # This stores the symptoms and appends
                symptom = row['short_description']
                sptm.append(symptom)

                # This stores the private log
                private_logg = None
                prv_log.append(private_logg)

                # This stores the solution
                sol = None
                soln.append(sol)

                # Caller
                caller = row['requester']['name']
                cal.append(caller)

                # Tenant
                tenant = None
                ten.append(tenant)

                # Email

                email = row['requester']['email_id']
                emails.append(email)

                # Location
                location = row['site']
                loc.append(location)

                # Medium
                medium = None
                med.append(medium)

                # Source
                source = None
                src.append(source)

                # Logged Time
                logg_time = row['created_time']['display_value']
                log_tm.append(logg_time)

                # Urgency
                urgency = row['is_overdue']
                urg.append(urgency)

                # Impact
                impact = row['subject']
                imp.append(impact)

                # Priority
                priority = row['priority']
                pr.append(priority)

                # Workgroup
                wrk_gp = row['requester']['department']
                wg.append(wrk_gp)

                # Assigned to
                assg_to = None
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
    print(len(incd_id),len(sptm),len(prv_log),len(cal),len(ten),len(emails),len(loc),len(med),len(src),len(log_tm),len(urg),len(imp),len(pr),len(wg),len(at),len(sw))
    # config.logger.info('Storing values in a dataframe')
    df_dict = {'Incident ID': incd_id, 'Description': sptm, 'Private Log': prv_log, 'Caller': cal, 'Tenant': ten, \
               'User_Mail': emails, 'Location': loc, 'Medium': med, 'Source': src, 'Logged Time': log_tm,
               'Urgency': urg, 'Impact': imp, 'Priority': pr, \
               'Work Group': wg, 'Assigned To': at, 'Service Window': sw,'MAC_ID':macid}  # ,'Resolution Code':rc,'Solution':soln,}
    
    df = pd.DataFrame(df_dict, index=None)

#     print('df unsorted is', df)
    df.sort_values(by='Incident ID',inplace=True)
#     df.to_csv('Incidents_no_pred.csv')
    print('df sorted is\n', df)

    #     df.to_excel('Incidents.xlsx',sheet_name='All_Incidents')

    # config.logger.info('Calling the prediction script for ticket classification')
    df=predicting_part.predictionsOnEachTicket(df)
    df.sort_values(by='Incident ID',inplace=True)
    # config.logger.info("Done")
    return df, num_of_tickets

# s = loginAndFetchTickets()

