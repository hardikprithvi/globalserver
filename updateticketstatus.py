from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import config
import threading
from flask import Flask,request,render_template
import pandas as pd
from check_licensing import checklicense,decrypt_message,load_key
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options 
import create_db
import configparser

config1 = configparser.ConfigParser()
config1.read('config_test.ini')

config1['DEFAULT']['login pass'] = decrypt_message(bytes(config1['DEFAULT']['login pass'],'utf-8'))
def updateTicket(df):
    try:
        config.logger.info('Logging into ITSM tool for ticket status update')
        options = Options() 
        options.headless = True
        options.add_argument("--window-size=1920,1200")
        driver = webdriver.Chrome(options=options,executable_path=ChromeDriverManager().install())
#         driver = webdriver.Chrome(ChromeDriverManager().install())
#         Gets the URL 
        print("opening browser")
        driver.get(config1["DEFAULT"]["website link"])
        driver.maximize_window()
        print("maximizing screen")
        time.sleep(3)
        
#         Finds the user name and password by id from HTML
        element = driver.find_element_by_id("txtLogin")
        element1 = driver.find_element_by_id("txtPassword")
        
#         Enters the user name and password
        element.send_keys(config1["DEFAULT"]["login id"])
        element1.send_keys(config1["DEFAULT"]["login pass"])
        
#         Clicks the login button
        driver.find_element_by_id("butSubmit").click()
        print("entered itsm")
    except Exception as e:
        pass

        config.logger.exception('Error in logging into ITSM tool for ticket status update '+str(e))

#     This is used to check if a duplicate login window pop ups, if it does press continue otherwise pass 

    try:
        if driver.find_element_by_class_name("TitlePanel").text == 'DUPLICATE LOGIN':
            driver.switch_to.frame(driver.find_element_by_tag_name("iframe"))
            driver.find_element_by_id("ContentPanel_btnContinue").click()
        else:
            pass
    except:
        print("okay")
    
    time.sleep(1)
    driver.find_element_by_id("IM").click()
    driver.find_element_by_id("IM_WORKGROUP_TICKETS").click()
    
    num_of_tickets = int(driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_lblCurrentRange"]').text.split()[-1].strip())
    print("accessing IM")
    for i in range(0,len(df)+1):
        print("inside for")
        try:
#             config.logger('Iterating over each ticket for updating status')
            in_id = int(df['Incident ID'][i])
            print(in_id)
            solu = df['Solution'][i]
            print(solu)
            stat = df['Status'][i]
            print(stat)
            print("Iterating Over Ticket",i+1)
            
            for j in range(1,num_of_tickets+1):
                print("inside for 2")
                incident=int(driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_gvMyTickets"]/tbody/tr['+str(j+2)+']/td[2]/div[2]/a[1]').text)
                if incident == in_id:
                    driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_gvMyTickets"]/tbody/tr['+str(j+2)+']/td[2]/div[2]/a[1]').click()
                    time.sleep(2)

                    # This clicks on the assigned to option
                    driver.find_element_by_xpath('//*[@id="s2id_BodyContentPlaceHolder_ddlAssignedExecutive"]/a/span[2]/b').click()
                    time.sleep(2)
                    afs= driver.find_element_by_xpath('//*[@id="s2id_autogen34_search"]')
                    afs.send_keys("AFS Automation")
                    time.sleep(2)
                    afs.send_keys(Keys.ENTER)
                    print("assign complete")

    #                     This clicks on  the communication panel
                    driver.find_element_by_xpath('//*[@id="aCommunication"]').click()

    #                     This fills the communication panel
                    text = driver.find_element_by_xpath('//*[@id="Communication"]/div/div[2]/div[3]/div[2]/div')
                    text.send_keys("Ticket Resolved")
                    print("communication panel")



    #                     Clicks on the resolved part 

                    driver.find_element_by_xpath('//*[@id="ticketdetail"]/div[2]/div/div[2]/div/div[1]/div/div/ul/li[5]/a').click()
                        #driver.find_element_by_xpath('//*[@id="ticketdetail"]/div[2]/div/div[2]/div/div[1]/div/div/ul/li[5]/a').text

                    time.sleep(10)
    #                     Clicks on the general panel
                    driver.find_element_by_xpath('//*[@id="general"]/a').click()


                    time.sleep(3)
    #                     This scrolls the window
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")



    #                     Clicks on the solution panel and fills it
                    driver.find_element_by_xpath('//*[@id="divSolutionRow"]/div[2]/div/div[2]/div').click()
                    time.sleep(2)
                    solution=driver.find_element_by_xpath('//*[@id="divSolutionRow"]/div[2]/div/div[2]/div')
                    print('Solution is ',solu)
                    if solu:
                        print("in if sol")
                        solution.send_keys(solu)
                    else:
                        print("in else sol")
                        solution.send_keys('Solution still Pending')
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


    #                     This clicks on the resolution code and selects  
#                     all_sol =['SELECT','Resolved','Completed With Errors','User not responding','Other Support Required','Out-of-Scope']

                    if stat=='Resolved':
                            driver.find_element_by_xpath('//*[@id="s2id_BodyContentPlaceHolder_ddlResolutionCode"]/a/span[2]/b').click()
                            time.sleep(3)
#                             driver.find_element_by_id("select2-result-label-172").click()
                            afs1= driver.find_element_by_id('s2id_autogen140_search')
                            afs1.send_keys("Resolved")
                            time.sleep(2)
                            afs1.send_keys(Keys.ENTER)
                            

#                             pyautogui.press("down")
#                             pyautogui.press("enter")
                            print("in if resolved")
                    else:
                            driver.find_element_by_xpath('//*[@id="s2id_BodyContentPlaceHolder_ddlResolutionCode"]/a/span[2]/b').click()
                            time.sleep(3)
                            afs1= driver.find_element_by_id('s2id_autogen140_search')
                            afs1.send_keys("Out-Of-Scope")
                            time.sleep(2)
                            afs1.send_keys(Keys.ENTER)
#                             pyautogui.press("down",presses=4)
#                             pyautogui.press("enter")
                            print("in else resolved")


                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)


    #                     This clicks on the violation panel 1 , if its is yes then it fills the text

                    if driver.find_element_by_xpath('//*[@id="General"]/div[2]/div/div[2]/div[2]/div/div[2]/label').text[-3:] == 'Yes':
                        print("in if Yes")
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        time.sleep(2)
                        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                        driver.find_element_by_xpath('//*[@id="iRespReasonOpener"]').click()
                        text1 = driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_txtRespViolationReason"]')
                        text1.send_keys('This happened because of system latency')
                        driver.find_element_by_xpath('//*[@id="divRespViolationReason"]/div[3]/input').click()
                    else:
                        print("else yes")
                        pass

    #                           This clicks on the violation panel 2 , if its is yes then it fills the text

                    if driver.find_element_by_xpath('//*[@id="General"]/div[2]/div/div[4]/div[2]/div/div[2]/label/span/span').text == 'Yes':
                        print("if yes")
                        driver.find_element_by_xpath('//*[@id="iResolReasonOpener"]').click()
                        text2 = driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_txtResolViolationReason"]')
                        text2.send_keys('This happened because of system latency')
                        driver.find_element_by_xpath('//*[@id="divResolViolationReason"]/div[3]/input').click()
                    else:
                        print("else yes")
                        pass

    #                     This clicks on the submit button
                    driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_btnSave"]').click()
                    print("submit clicked")

    #                     This clicks on the final ok button
                    driver.current_window_handle
                    driver.find_element_by_xpath('/html/body/div[9]/div/div/div[2]/button').click() 
                    print("final okay button")


                    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH,'//*[@id="divMenu"]/nav/ul/li[4]')))
                    driver.find_element_by_xpath('//*[@id="divMenu"]/nav/ul/li[4]').click()
                    driver.find_element_by_xpath('//*[@id="IM_WORKGROUP_TICKETS"]').click()


                else:
                    print("Incident id no match else")
                    continue


        except Exception as e:
            pass
#             config.logger.exception('Error in updating ticket status into ITSM tool '+str(e)) 
            print("fail updation")
    print("trigger logout process")
    driver.find_element_by_xpath('//*[@id="imgProfile"]').click()
    driver.find_element_by_xpath('//*[@id="hrefLogout"]').click()
    driver.quit()

def updateTicket_2(ticket_id,status,solution):
    config.logger.exception('In update ticket part')
#     df = create_db.get_data()
    query = "select * from tickets where `Incident ID` ='"+ticket_id+"';"
    df = create_db.fetchquery(query)
#     print(df)
    df.loc[df["Incident ID"]==ticket_id , 'Status'] = status
    df.loc[df["Incident ID"]==ticket_id , 'Solution'] = solution
        
    ret = create_db.update(df)
    config.logger.exception('data updated in db')

    updateTicket(df.loc[df.Status =="Resolved"]) 
    config.logger.exception('ticket updated in itsm')

                  