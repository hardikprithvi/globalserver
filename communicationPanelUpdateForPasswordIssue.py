from selenium import webdriver
import time
import configparser
config1 = configparser.ConfigParser()
config1.read('config_test.ini')
def communicationPanelUpdate(inc_id):
    driver = webdriver.Chrome('chromedriver.exe')
    # Gets the URL 
    driver.get(config1["DEFAULT"]["website link"])
    # Finds the user name and password by id from HTML
    element = driver.find_element_by_id("txtLogin")
    element1 = driver.find_element_by_id("txtPassword")
    # Enters the user name and password
    element.send_keys(config1["DEFAULT"]["login id"])
    element1.send_keys(config1["DEFAULT"]["login pass"])
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
    
        
    # Calculating number of tickets
    num_of_tickets = int(driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_lblCurrentRange"]').text.split()[-1].strip())
    for j in range(1,num_of_tickets+1):
        incident=int(driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_gvMyTickets"]/tbody/tr['+str(j+1)+']/td[2]/div[2]/a[1]').text)
        if incident == inc_id:
            driver.find_element_by_xpath('//*[@id="BodyContentPlaceHolder_gvMyTickets"]/tbody/tr['+str(j+1)+']/td[2]/div[2]/a[1]').click()
            
            # This clicks on  the communication panel
            driver.find_element_by_xpath('//*[@id="aCommunication"]').click()
            
            # This fills the communication panel
            text = driver.find_element_by_xpath('//*[@id="Communication"]/div/div[1]/div[3]/div[2]/div')
            text.send_keys("Comments have been put in the communication tab of ITSM tool. Please log in and check.")
            
    driver.find_element_by_xpath('//*[@id="imgProfile"]').click()
    driver.find_element_by_xpath('//*[@id="hrefLogout"]').click()
    driver.quit()