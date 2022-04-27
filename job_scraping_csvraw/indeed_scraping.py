import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd
from selenium.common.exceptions import TimeoutException
import re

ser = Service("../driver/chromedriver")
op = webdriver.ChromeOptions()
s = webdriver.Chrome(service=ser, options=op)
s.maximize_window()

df = pd.DataFrame(columns=["Title","Company","SalaryOne","SalaryTwo","Location","Summary","Qualification","Role&Responsibilities"])

state_element = True
job_title = "beatmaker"

for page in range(0,130,10):
 
    s.get("https://ph.indeed.com/jobs?q={}&start={}".format(job_title,page))
   
    job_listing =  WebDriverWait(s, 30).until(EC.presence_of_element_located((By.ID, "resultsBody")))
    job_listing.click()
    wait = WebDriverWait(s, 10)

    for i in s.find_elements(By.CLASS_NAME,'tapItem'):
        qualification = []
        roles_responsibilities = []
        soup_two = bs(i.get_attribute("innerHTML"),"html.parser")
        try:
            i.click()
            
        except:
            close_button = s.find_elements(By.CLASS_NAME,'popover-x-button-close')[0]
            close_button.click()
            i.click()

        try:
            title = soup_two.find("h2",class_="jobTitle").text.replace("\n","").strip()
          
        except:
            title = "None"

        try:
            company_name = soup_two.find("span",class_="companyName").text.replace("\n","").strip()
        except:
            company_name = "None"
        
        try:
            company_location = soup_two.find("div",class_="companyLocation").text.replace("\n","").strip()
        except:
            company_location = "None"

        try:

            summary = soup_two.find("div",class_="job-snippet").find('li').text
        except:
            summary = "None"

        try:
            salary = soup_two.find("div",class_="salary-snippet").find("span").text

        except:
            salary = "None"

        try:
            salary_two = soup_two.find("div",class_="salary-snippet-container").find("div",class_="attribute_snippet").text 
        except:
            salary_two = "None"

        section = wait.until(EC.frame_to_be_available_and_switch_to_it((By.XPATH, "//iframe[@id='vjs-container-iframe']")))
        
        # try:
        #     job_desc = WebDriverWait(s,1).until(EC.frame_to_be_available_and_switch_to_it((By.ID, 'jobDescriptionText')))
        #     parent = s.find_element(By.ID, 'jobDescriptionText')
        # except TimeoutException:
        parent = s.find_element(By.ID, 'jobDescriptionText')
    
        soup = bs(parent.get_attribute("innerHTML"),"html.parser")

        try:
            job_type = soup.find_all("div",class_='jobsearch-JobDescriptionSection-sectionItem')
        except:
            job_type = "None"
        
        print(job_type)

        try:
            li_tag = soup.find_all("li")
        except:
            li_tag = "None"

        for li in li_tag:
            qualification.append(li.text)

        try:
            p_tag = soup.find_all("p")
        except:
            p_tag = "None"

        for p in p_tag:
            roles_responsibilities.append(p.text)

        s.switch_to.default_content()
        df = df.append({'Title':title,'Company':company_name,"SalaryOne":salary,"SalaryTwo":salary_two,"Location":company_location,"Summary":summary, "Qualification":qualification,"Role&Responsibilities":roles_responsibilities},ignore_index=True)

    df.to_csv("Indeed-{}.csv".format(job_title),index=False)
        
    
s.close()    
           
    
        
        

        

          


    
  

