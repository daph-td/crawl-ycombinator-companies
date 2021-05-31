# Standard imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import csv
print('- Finish importing standard packages')

# setup selenium webdriver
opt = webdriver.ChromeOptions()
#opt.add_extension("Block-image_v1.1.crx")
opt.add_argument('--disable-gpu')
opt.add_argument("--window-size=1920,1080")
opt.add_argument("--start-maximized")
opt.add_argument('--disable-dev-shm-usage')
opt.add_argument('--no-sandbox')
opt.add_argument('--ignore-certificate-errors')
#opt.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36")
driver = webdriver.Chrome(options=opt)

# setup wait
wait = WebDriverWait(driver, 10)

URL = 'https://www.ycombinator.com/companies/?batch=W21&batch=S20&batch=W20&batch=S19&batch=W19&industry=Education'
driver.get(URL)

def GetProjectURL():
    page_source = BeautifulSoup(driver.page_source)
    projects = page_source.find_all('a', class_ = 'styles-module__company___1UVnl no-hovercard')
    all_project_URL = []
    for project in projects:
        project_ID = project.get('href')
        project_URL = "https://www.ycombinator.com" + project_ID
        if project_URL not in all_project_URL:
            all_project_URL.append(project_URL.lower())
    return all_project_URL

URLs_all_page_clean = GetProjectURL()
print(URLs_all_page_clean, len(URLs_all_page_clean))

# Scrape the data of 1 Linkedin profile, and write the data to a .CSV file
with open('ycom_edtech1920.csv', 'w',  newline = '') as file_output:
    headers = ['URL']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader()
    for linkedin_URL in URLs_all_page_clean:
        writer.writerow({headers[0]:linkedin_URL})

print('Mission Completed!')