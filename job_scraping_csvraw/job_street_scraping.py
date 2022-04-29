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

df = pd.DataFrame(columns=["Title","Company","Location","Summary","Salary","Qualification & Skills","Role and Responsibilities","Job Type","Company Profile&Job Desc", "Career Level", "Benefits","Company Size"])

#job = ["artist", "creative-director","game-designer","graphic-designer","illustrator","motion-graphic-artist","multimedia-artist","musician","producer","singer","sound-engineer"]
job = ["sound-engineer"]
for j in range(len(job)):

    for page in range(2,20):
        
        url = "https://www.jobstreet.com.ph/en/job-search/{}-jobs/{}/".format(job[j],page)
        s.get("https://www.jobstreet.com.ph/en/job-search/{}-jobs/{}/".format(job[j],page))

        job_lists = WebDriverWait(s,30).until(EC.presence_of_element_located((By.XPATH, "//div[@data-automation='jobListing']")))
        
        html_job_lists = s.find_element(By.XPATH, "//div[@data-automation='jobListing']")
        number_of_cards = html_job_lists.find_elements(By.TAG_NAME, "article")
    
        for card in range(0,len(number_of_cards)):
            job_card = WebDriverWait(s,30).until(EC.element_to_be_clickable((By.XPATH, "//article[@data-automation='job-card-{}']".format(card))))
            try:
                job_card.click()
            except:
                s.execute_script("window.scrollBy(0,200);")   
                #job_card.click()

            while s.current_url != url:
                time.sleep(1)
                #s.get("https://www.jobstreet.com.ph/en/job-search/{}-jobs/{}/".format(job[j],page))
                s.back()
                #s.execute_script("window.history.go(-1)")

            description = WebDriverWait(s,30).until(EC.presence_of_element_located((By.XPATH, "//div[@data-automation='jobDescription']")))
            if(description):
                
                job_descriptions = s.find_element(By.XPATH, "//div[@data-automation='jobDescription']")
                soup_one = bs(job_descriptions.get_attribute("innerHTML"), "html.parser")
                job_details = s.find_element(By.XPATH, "//div[@data-automation='detailsTitle']")  
                soup_two = bs(job_details.get_attribute("innerHTML"),"html.parser")

                details = s.find_element(By.XPATH, "//div[@class='sx2jih0 _17fduda0 _17fduda3']")
                soup_three = bs(details.get_attribute("innerHTML"),"html.parser")
                
                company_location = soup_three.find_all("span", class_="sx2jih0 zcydq84u _18qlyvc0 _18qlyvc1x _18qlyvc1 _18qlyvca")
                
                # -------- EXTRACTING DATA ---------- # 
                job_title = soup_two.find("h1").text
                company_name =soup_two.find("span").text
                location = company_location[0].text
            
                if "PHP" not in company_location[1].text:
                    salary = "None"
                else:
                    salary = company_location[1].text

                try:
                    summary = soup_one.find("li").text
                except:
                    summary = "None"

                qualification = soup_one.find_all("li")
                responsibilities = soup_one.find_all("p")

                additional_info = s.find_element(By.XPATH, "//div[@class='sx2jih0 zcydq86q zcydq86v zcydq86w zcydq87q zcydq87v zcydq87w zcydq896 zcydq886 _18qlyvc14 _18qlyvc17 zcydq832 zcydq835']")
                soup_four = bs(additional_info.get_attribute("innerHTML"),"html.parser")
                career_level = soup_four.find_all(text=re.compile("Experienced"))
                benefits = soup_four.find_all(text=re.compile("Medical"))
                company_size = soup_four.find_all(text=re.compile("Employees"))
                job_type =  soup_four.find_all(text=re.compile("Time"))
                company_overview = soup_four.find_all("div",class_="YCeva_0")
                c_sizes = None
                career = None
                for cs in company_size:
                    if "-" not in cs:
                        c_sizes = "None"
                    else:
                        c_sizes = cs
                
                for cl in career_level:
                    if "Experience" not in cl:
                        career = "None"
                    else:
                        career = cl
               
                df = df.append({"Title":job_title,"Company":company_name,"Location":location,"Summary":summary,"Salary":salary,"Qualification & Skills":[q.text for q in qualification],"Role and Responsibilities":[r.text for r in responsibilities],"Job Type":job_type,"Company Profile&Job Desc":[co.find("div").text for co in company_overview], "Career Level":career, "Benefits":benefits,"Company Size":c_sizes},ignore_index=True)
    
        df.to_csv("Jobstreet-{}.csv".format(job[j]),index=False)

s.close()    

