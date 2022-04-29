import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
import pandas as pd
import re

ser = Service("../driver/chromedriver")
op = webdriver.ChromeOptions()
s = webdriver.Chrome(service=ser, options=op)
s.maximize_window()


s.get("https://www.linkedin.com/jobs/search/?f_WT=2&geoId=103121230&keywords=artist&location=Philippines&start=0&currentJobId=3030456923&position=25&pageNum=0")

main_content = WebDriverWait(s,10).until(EC.presence_of_element_located((By.ID, "main-content")))
ul_content = s.find_element(By.CLASS_NAME,"jobs-search__results-list")


try:
    for li in ul_content.find_elements(By.TAG_NAME, "li"):
       
        li.click()
        
        soup_one = bs(li.get_attribute("innerHTML"),"html.parser")
        job_title = soup_one.find('h3',class_="base-search-card__title").text
        company_name = soup_one.find("h4",class_='base-search-card__subtitle').text
        company_location = soup_one.find('span',class_="job-search-card__location").text
        print(company_location)
    
        # Main Details
        #main_details = WebDriverWait(s,10).until(EC.presence_of_element_located((By.CLASS_NAME,"base-serp-page__content")))
        wait_main = s.find_element(By.CLASS_NAME,"base-serp-page__content")
        print(wait_main)

except StopIteration:
    print("Done")
   
