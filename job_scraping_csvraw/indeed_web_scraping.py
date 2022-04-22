import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd

ser = Service("driver/chromedriver")
op = webdriver.ChromeOptions()
s = webdriver.Chrome(service=ser, options=op)
s.maximize_window()

df = pd.DataFrame(columns=["Title","Company","Location","Summary"])
for page in range(0,30,10):
    time.sleep(10)
    s.get("https://ph.indeed.com/jobs?q=sound%20engineer&start={}".format(page))
    time.sleep(30)
    results = s.find_elements(By.CLASS_NAME,'result')

    for i in results:
        soup_two = bs(i.get_attribute("innerHTML"),"html.parser")
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
            summary = None

        element = s.find_element(By.CLASS_NAME, "tapItem")

        try:
            element.click()
        except:
            close_button = s.find_elements_by_class_name('popover-x-button-close')[0]
            close_button.click()
            element.click()	

        df = df.append({'Title':title,'Company':company_name,"Location":company_location,"Summary":summary},ignore_index=True)
    
    df.to_csv("sound-engineer.csv",index=False)	