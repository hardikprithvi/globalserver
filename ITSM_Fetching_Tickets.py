import pandas as pd
from selenium import webdriver
import time
import threading
from selenium.webdriver.common.keys import Keys
import predicting_part
import config
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options 
import create_db
from check_licensing import checklicense,decrypt_message,load_key
import configparser
config1 = configparser.ConfigParser()
config1.read('config_test.ini')

config1['DEFAULT']['login pass'] = decrypt_message(bytes(config1['DEFAULT']['login pass'],'utf-8'))
def loginAndFetchTickets(macid):
    try:
    
        config.logger.info('Logging into ITSM tool for ticket fetching')
        # headless access
        options = Options() 
        options.headless = True
        options.add_argument("--window-size=1920,1200")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--ignore-certificate-errors')
        driver = webdriver.Chrome(options=options,executable_path=ChromeDriverManager().install())
        # Gets the URL 
        print("Opening browser with ITSM")
        # Gets the URL 
        driver.get(config1["DEFAULT"]["website link"])
        print("maxamize window")
        driver.maximize_window()
        
        time.sleep(3)
        
        # Finds the user name and password by id from HTML
        element = driver.find_element_by_id("txtLogin")
        element1 = driver.find_element_by_id("txtPassword")
        
        # Enters the user name and password
        element.send_keys(config1["DEFAULT"]["login id"])
        element1.send_keys(config1["DEFAULT"]["login pass"])
        print("inside itsm")
        # Clicks the login button
        driver.find_element_by_id("butSubmit").click()
        
        
        # This is used to check if a duplicate login window pop ups, if it does press continue otherwise pass 
        try:
            if driver.find_element_by_class_name("TitlePanel").text == 'DUPLICATE LOGIN':
                driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
                driver.find_element_by_id("ContentPanel_btnContinue").click()
            else:
                pass
        except:
            print(" ")
        
        time.sleep(1)
        driver.find_element_by_id("IM").click()
        driver.find_element_by_id("IM_WORKGROUP_TICKETS").click()
        time.sleep(6)
    except Exception as e:
        
        config.logger.exception('Error in logging into ITSM tool for ticket fetching '+str(e))
        
    
    incd_id =[]
    sptm =[]
    prv_log=[]
    soln=[]
    cal =[]
    ten =[]
    loc=[]
    med=[]
    src =[]
    log_tm =[]
    urg=[]
    imp=[]
    pr=[]
    wg=[]
    at=[]
    sw=[]
    rc=[]
    emails=[]
    # Calculating number of tickets
    num_of_tickets = int(driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_lblCurrentRange"]').text.split()[-1].strip())
    for i in range(1,2):
        print("fetching ticket",i)
        try:
            config.logger.info('Finding ticket attributes and storing it in a dataframe')
            # This checks if the ticket is new
            # //*[@id="BodyContentPlaceHolder_gvMyTickets"]/tbody/tr[3]/td[4]/h4/span
            # //*[@id="BodyContentPlaceHolder_gvMyTickets"]/tbody/tr[3]/td[2]/div[2]/a[1]
            if driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_gvMyTickets"]/tbody/tr['+str(i+2)+']/td[4]/h4/span').text == 'New':
               # //*[@id="BodyContentPlaceHolder_gvMyTickets"]/tbody/tr[3]/td[4]/h4
                # This stores the incident id
                inc_id = driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_gvMyTickets"]/tbody/tr['+str(i+2)+']/td[2]/div[2]/a[1]').text
                
                #This clicks on the incident id
                driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_gvMyTickets"]/tbody/tr['+str(i+2)+']/td[2]/div[2]/a[1]').click()
                time.sleep(2)
               # //*[@id="ticketdetail"]/div[2]/div/div[2]/div/div[1]/div/div/ul/li[2]
                # This clicks on the assigned
                driver.find_element_by_xpath('//*[@id="ticketdetail"]/div[2]/div/div[2]/div/div[1]/div/div/ul/li[2]').click()
                
                # This clicks on the assigned to option
                driver.find_element_by_xpath('//*[@id="s2id_BodyContentPlaceHolder_ddlAssignedExecutive"]/a/span[2]/b').click()
                time.sleep(2)
                afs= driver.find_element_by_xpath('//*[@id="s2id_autogen34_search"]')
                afs.send_keys("AFS Automation",Keys.ENTER)
                #pyautogui.press("down")
                #pyautogui.press("enter")
                
                # This clicks on  the communication panel
                driver.find_element_by_xpath('//*[@id="aCommunication"]').click()
                
                # This fills the communication panel
                text = driver.find_element_by_xpath('//*[@id="Communication"]/div/div[2]/div[3]/div[2]/div')
                text.send_keys("Ticket is in progress")
                
                #my comment
                # Clicks on the resolved part 
                #driver.find_element_by_xpath('//*[@id="ticketdetail"]/div[2]/div/div[2]/div/div[1]/div/div/ul/li[5]/a').click()
                
                # Clicks on the general panel
                driver.find_element_by_xpath('//*[@id="general"]/a').click()
               
                
              #  # This clicks on the violation panel , if its is yes then it fills the text
              #  if driver.find_element_by_xpath('//*[@id="General"]/div[2]/div/div[2]/div[2]/div/div[2]/label').text[-3:] == 'Yes':
              #      driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
              #      time.sleep(2)
              #      driver.find_element_by_xpath('//*[@id="iRespReasonOpener"]').click()
              #      text1 = driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_txtRespViolationReason"]')
              #      text1.send_keys('This happened because i was sleeping')
              #      driver.find_element_by_xpath('//*[@id="divRespViolationReason"]/div[3]/input').click()
              #  else:
              #      pass
              #  
                # Clicks on the solution panel and fills it
               # solution = driver.find_element_by_xpath('//*[@id="divSolutionRow"]/div[2]/div/div[2]/div')
               # solution.send_keys("Ticket Resolved")
                
                # This scrolls the window
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                
                
                # This clicks on the resolution code and selects resolved 
                #driver.find_element_by_xpath('//*[@id="s2id_BodyContentPlaceHolder_ddlResolutionCode"]/a/span[2]/b').click()
                #pyautogui.press("down")
                #pyautogui.press("enter")
                
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                # This fills the asset details
                asset_id = driver.find_element_by_xpath('//*[@id="txt_26"]')
                asset_id.send_keys("Asset_id")
                
                # This fills the Serial Number
                serial_no = driver.find_element_by_xpath('//*[@id="txt_25"]')
                serial_no.send_keys("Serial_no")
                
                
                time.sleep(5)
    
                
                
                # This clicks on the violation panel , if its is yes then it fills the text
                if driver.find_element_by_xpath('//*[@id="General"]/div[2]/div/div[2]/div[2]/div/div[2]/label').text[-3:] == 'Yes':
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    driver.find_element_by_xpath('//*[@id="iRespReasonOpener"]').click()
                    text1 = driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_txtRespViolationReason"]')
                    text1.send_keys('This happened because of system latency')
                    driver.find_element_by_xpath('//*[@id="divRespViolationReason"]/div[3]/input').click()
                else:
                    pass
                
                
               
    
                # This appends the incident id
                incd_id.append(inc_id)
                
                # This stores the symptoms and appends
                symptom = driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_lblSymptomDisplay"]').text
                sptm.append(symptom)
                
                #This stores the private log
                driver.find_element_by_xpath('//*[@id="aCommunication"]').click()
                private_logg = driver.find_element_by_xpath('//*[@id="Communication"]/div/div[2]/div[3]/div[2]/div').text
                prv_log.append(private_logg)
                
                # This stores the solution
                driver.find_element_by_xpath('//*[@id="general"]/a').click()
                sol = driver.find_element_by_xpath('//*[@id="divSolutionRow"]/div[2]/div/div[2]/div').text
                soln.append(sol)
                
                #Caller
                caller = driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_ucUserInformation_lblName"]').text
                cal.append(caller)
                
                
                #Tenant
                tenant =driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_ucUserInformation_lblCustomer"]').text
                ten.append(tenant)
                
                #Email
                
                email=driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_ucUserInformation_lblEmail"]/a').text
                emails.append(email)
                
                
                # Location
                location=driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_ucUserInformation_lblLocation"]').text
                loc.append(location)
                
                
                # Medium
                medium =driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_lblMediumDisplay"]').text
                med.append(medium)
                
                # Source
                source=driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_lblSourceDisplay"]').text
                src.append(source)
                
                # Logged Time
                logg_time=driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_lblLogTime"]').text
                log_tm.append(logg_time)        
                
                # Urgency 
                urgency=driver.find_element_by_id('s2id_BodyContentPlaceHolder_ddlUrgency').text
                urg.append(urgency)
                
                # Impact
                impact=driver.find_element_by_xpath('//*[@id="s2id_BodyContentPlaceHolder_ddlImpact"]/a').text
                imp.append(impact)
                
                # Priority
                priority=driver.find_element_by_id('s2id_BodyContentPlaceHolder_ddlPriority').text
                pr.append(priority)
                
                # Workgroup
                wrk_gp=driver.find_element_by_id('s2id_BodyContentPlaceHolder_ddlWorkgroup').text   
                wg.append(wrk_gp)
                
                # Assigned to
                assg_to=driver.find_element_by_id('s2id_BodyContentPlaceHolder_ddlAssignedExecutive').text
                at.append(assg_to)
                
                
                #Service window
                serv_win=driver.find_element_by_id('s2id_BodyContentPlaceHolder_ddlSLA').text
                sw.append(serv_win)
                
                # Resolution code
                resol_code=driver.find_element_by_id('s2id_BodyContentPlaceHolder_ddlResolutionCode').text
                rc.append(resol_code)
                
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
                
                #This clicks on the submit button
                #driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_btnSave"]').click()
                #time.sleep(10)
                
                #This clicks on the final ok button
                #driver.current_window_handle
                #driver.find_element_by_xpath('/html/body/div[9]/div/div/div[2]/button').click()
                
                time.sleep(5)
                
                driver.find_element_by_id("IM").click()
                driver.find_element_by_id("IM_WORKGROUP_TICKETS").click()
                            
                
            else:
                continue
        
        except Exception as e:
            print("Error in storing attributes"+str(e))
            config.logger.exception('Error in storing attributes of a ticket '+str(e))
        
        
        
    config.logger.info('Storing values in a dataframe')       
    df_dict ={'Incident ID':incd_id, 'Description':sptm ,'Private Log':prv_log ,'Caller':cal,'Tenant':ten,\
                  'User_Mail':emails,'Location':loc,'Medium':med,'Source':src,'Logged Time':log_tm,'Urgency':urg,'Impact':imp,'Priority':pr,\
                  'Work Group':wg,'Assigned To':at,'Service Window':sw,'MAC_ID':macid}#,'Resolution Code':rc,'Solution':soln,}
    df = pd.DataFrame(df_dict, index = None)    
    
    print('df unsorted is\n',df)
    #df.sort_values(by='Incident ID',inplace=True)
#     df.to_csv('Incidents_no_pred.csv')
    print('df sorted is\n',df)
    
#     df.to_excel('Incidents.xlsx',sheet_name='All_Incidents')
    
    config.logger.info('Calling the prediction script for ticket classification')
    df=predicting_part.predictionsOnEachTicket(df)
    df.sort_values(by='Incident ID',inplace=True)
    
    
    driver.find_element_by_xpath('//*[@id="imgProfile"]').click()
    driver.find_element_by_xpath('//*[@id="hrefLogout"]').click()
    driver.quit()
    print("logged out")
    #threading.Timer(180, loginAndFetchTickets).start()
    
    return df,num_of_tickets
    