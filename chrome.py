from selenium import webdriver
import os
from selenium.webdriver.chrome.options import Options
import time 

options = webdriver.ChromeOptions()
options.add_extension('extension.crx')

url = 'http://youtube.com'

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))
DRIVER_BIN = os.path.join(PROJECT_ROOT, "chromedriver")

def start():
    driver = webdriver.Chrome(executable_path = DRIVER_BIN,chrome_options=options)
    driver.get(url)
    return driver

def end(driver):
    driver = driver.quit()
    return print('ended')

driver = start()
time.sleep(10)
print("browser running")
end(driver)