from selenium import webdriver
from selenium.webdriver.chrome.service import Service
ser = Service("driver/chromedriver")
op = webdriver.ChromeOptions()
s = webdriver.Chrome(service=ser, options=op)
s.get("https://www.google.com")