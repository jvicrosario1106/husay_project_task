import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

ser = Service("driver/chromedriver")
op = webdriver.ChromeOptions()
s = webdriver.Chrome(service=ser, options=op)
s.maximize_window()
s.get("https://www.google.com")

job_list = []
def generate_url(job_title,page):
    url_template = "https://www.jobstreet.com.ph/en/job-search/{}-jobs/{}/"
    format_url = url_template.format(job_title,page)
    return format_url

job_name = "Multimedia Artist" # You can change this

for i in range(1,3):
    
    url_template = "https://www.jobstreet.com.ph/en/job-search/{}-jobs/{}/".format(job_name,i)
    s.get(url_template)
    time.sleep(30)

    for job_title in WebDriverWait(s, 10).until(EC.presence_of_all_elements_located((By.XPATH, "//h1[@class='sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc3 _18qlyvca']"))):
        try:
            job_title.click()
            s.execute_script("window.scrollBy(0,240)")
            
        except:
            s.execute_script("window.scrollBy(0,260)")
            job_title.click()
