import time
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd


ser = Service("../driver/chromedriver")
op = webdriver.ChromeOptions()
driver = webdriver.Chrome(service=ser, options=op)
df = pd.DataFrame(columns=["Title","Description","Location","Skill","Est.Proj-Budget", "Job Type", "Contractor Tier","Duration"])
# headers = {
#     "User-agent": 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36',
#     "cookie": "visitor_id=112.211.111.131.1650499633942000; __zlcmid=19bkrnQIcaHNKdO; lang=en; lang=en; cookie_prefix=; cookie_domain=.upwork.com; device_view=full; g_state={'i_p':1650508862899,'i_l':1}; G_ENABLED_IDPS=google; recognized=53a4c5af; console_user=53a4c5af; user_uid=1432975559892008960; master_access_token=3015833f.oauth2v2_ec865780710eb73c31f24fbc8c73a4c7; oauth2_global_js_token=oauth2v2_37493d6138105d49f7bf2181a31076c8; company_last_accessed=d1006326284; current_organization_uid=1432975559892008961; user_oauth2_slave_access_token=3015833f.oauth2v2_ec865780710eb73c31f24fbc8c73a4c7:1432975559892008960.oauth2v2_57b509fe07f13818e32f76f1c4b084c7; channel=other; JobSearchUI_tile_size_1432975559892008960=medium; spt=613fab5d-85d0-484a-9673-6cf82682f3a2; restriction_verified=1; vjd_gql_token=oauth2v2_8d8e8ca3b805d2fa7a0f06bbb152caa9; visitor_signup_gql_token=oauth2v2_c42c0047c18cd930061523e58cee1675; OptanonConsent=isGpcEnabled=1&datestamp=Thu+Apr+21+2022+09:23:58+GMT+0800+(Philippine+Standard+Time)&version=6.28.0&isIABGlobal=false&hosts=&consentId=2579700d-905a-47f3-88d5-0fe29db4101d&interactionCount=1&landingPath=NotLandingPage&groups=C0001:1,C0002:0,C0003:1,C0004:0&AwaitingReconsent=false; vps_gql_token=oauth2v2_ded048677fcfd8274d983cc0e3dcafb8; visitor_ui_gql_token=oauth2v2_0a818d9e30bc88e03bc4dddd78aeb9e6; visitor_gql_token=oauth2v2_c39eace873c2782ab19ed89fbee9c100; _pxhd=T6rF/RRCgLuuEGq4V00fDIKrM-qC8uvpyEssQI1ZMFb40awhKbSrcqmBBN8gG28Y0Fr787qiM0getknPnucATA==:GLrI6AjDK/aVZadEaLe8OmHj1d10C9UHskTDgwHKQEuPYlFUfI0C65xAUYIMVrAUovR/RVAUXkGKmRCY7OZQGylOTWW8rfXy83lxfoyXyME=; odesk_signup.referer.raw=https://www.google.com/; __cfruid=9c9c2c9463fb98619f23628eb852e8c8e211597e-1650539079; XSRF-TOKEN=0f16c6de7101eb66a9422caf9c4851d6; _sp_ses.2a16=*; __cf_bm=oJPFfzVopa7uaHipX2TaLIo0vtErUMvHbcbFVC07fSk-1650579737-0-AWU6aQn+9J6PUbxIViE51FjpXmckpW2VsfWh8a+IaLhD6P/bNPQ1o6OpiUDeH+0PUhwyv2dI7svgtbT4cg3jdGw=; enabled_ff=!OTBnr,OTBnrOn,!SSINav,!CI10270Air2Dot5QTAllocations,!air2Dot76Qt,CI11132Air2Dot75,CI9570Air2Dot5,!CI10857Air3Dot0,!CI12577UniversalSearch,!air2Dot76; _sp_id.2a16=57a92868-d7a4-4412-98fa-b218b2d6c6da.1650501700.4.1650580274.1650541275.9cf70419-8d60-49a7-abc0-220e196be1b0",

# }
job = ["artist", "creative%20director","game%20designer","graphic%20designer","illustrator","motion%20graphic%20artist","multimedia%20artist","musician","producer","singer","sound%20engineer"]
page = 8
jobs = job[10]
skills = []
template_url = "https://www.upwork.com/nx/jobs/search/?q={}&sort=recency&page={}"
final_url = template_url.format(jobs,page)
driver.get(final_url)
time.sleep(3)
list = WebDriverWait(driver,30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "up-card-hover")))    

tiles = driver.find_elements(By.CLASS_NAME, "up-card-hover")
for i in tiles:

    soup = bs(i.get_attribute("innerHTML"),"html.parser")
    
    job_title = soup.find("h4",class_="job-tile-title").text.replace("\n","").strip()
    job_description =  soup.find("span",{'data-test': 'job-description-text'}).text.replace("\n","").strip()
    print(job_title)
    try:
        skill = soup.find("div", class_="up-skill-wrapper").find_all("a")
    except:
        skill = []
    
    try:
        budget =  soup.find("span", {'data-test': 'budget'}).text
    except:
        budget = "None"
    try:
        job_type = soup.find("strong",{'data-test':'job-type'}).text
    except:
        job_type = "None"

    try:
        contractor_tier = soup.find("span",{'data-test':'contractor-tier'}).text
    except:
        contractor_tier = "None"

    try:
        duration = soup.find("span",{'data-test':'duration'}).text
    except:
        duration = "None"

    try:
        location = soup.find("small", {'data-test':'client-country'}).find("strong").text
    except:
        location = "None"

    if len(skill) > 0 :
        for s in skill:
            skills.append(s.text)

    df = df.append({'Title':job_title,'Description':job_description,"Location":location,"Skill":skills, "Est.Proj-Budget":budget, "Job Type":job_type, "Contractor Tier":contractor_tier,"Duration":duration},ignore_index=True)
    
df.to_csv("upwork-{}-{}.csv".format(jobs, page),index=False)

driver.close()

  