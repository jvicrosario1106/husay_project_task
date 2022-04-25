import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd

ser = Service("../driver/chromedriver")
op = webdriver.ChromeOptions()
s = webdriver.Chrome(service=ser, options=op)
s.maximize_window()

df = pd.DataFrame(columns=["Title","Company","Location","Summary"])

for page in range(2,4):
    url = "https://www.jobstreet.com.ph/en/job-search/{}-jobs/{}/".format("illustrator",page)
    s.get("https://www.jobstreet.com.ph/en/job-search/{}-jobs/{}/".format("illustrator",page))

    job_lists = WebDriverWait(s,30).until(EC.presence_of_element_located((By.XPATH, "//div[@data-automation='jobListing']")))
    
    html_job_lists = s.find_element(By.XPATH, "//div[@data-automation='jobListing']")
    number_of_cards = html_job_lists.find_elements(By.TAG_NAME, "article")
    
    for card in range(0,len(number_of_cards)):
        job_card = WebDriverWait(s,30).until(EC.element_to_be_clickable((By.XPATH, "//article[@data-automation='job-card-{}']".format(card))))          
        job_card.click()

        while s.current_url != url:
            time.sleep(2)
            s.execute_script("window.history.go(-1)")

        description = WebDriverWait(s,30).until(EC.presence_of_element_located((By.XPATH, "//div[@data-automation='jobDescription']")))
        if(description):
            job_descriptions = s.find_element(By.XPATH, "//div[@data-automation='jobDescription']")
            soup = bs(job_descriptions.get_attribute("innerHTML"), "html.parser")
            print(soup.prettify())    

        time.sleep(1)

                   
s.close()    
           
    
        
        

        

          


    
  

