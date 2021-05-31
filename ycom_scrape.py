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

def getFounders(founder_card):
    founder_name = founder_card.find('div', class_='font-bold').get_text()
    try:
        founder_social = founder_card.find('div', class_='social-links')
        founder_linkedin = founder_social.find('a', class_='social linkedin').get('href')
        return founder_name, founder_linkedin
    except AttributeError:
        return founder_name, 'NA'

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
with open('YC_EdTech_1920_3.csv', 'w',  newline = '') as file_output:
    headers = [
        'ycomURL', 'company_name',
        'company_tagline', 'company_description', 
        'URL', 'founded', 
        'team_size', 'location',
        'founder_name_1', 'founder_linkedin_1',
        'founder_name_2', 'founder_linkedin_2',
        'founder_name_3', 'founder_linkedin_3']
    writer = csv.DictWriter(file_output, delimiter=',', lineterminator='\n',fieldnames=headers)
    writer.writeheader()
    for ycomURL in URLs_all_page_clean:
        print('\n--- Start scraping ...')
        driver.get(ycomURL)
        sleep(10)
        content = driver.page_source.encode('utf-8').strip()
        company_page_source = BeautifulSoup(content, "html.parser")
        company_name = company_page_source.find('h1', class_='font-bold').get_text()
        print(company_name)
        company_tagline = company_page_source.find('h3', style='font-size:1.5em;margin-bottom:10px;').get_text()
        print(company_tagline)
        company_description = company_page_source.find('p', class_='pre-line').get_text()
        print(company_description)
        company_url = company_page_source.find_all('div', class_='links')
        for link in company_url[1]:
            URL = link.get('href')
        print(URL)
        highlight_box = company_page_source.find('div', class_='highlight-box')
        highlight_info = highlight_box.find('div', class_='facts').find_all('span', class_='right')
        founded = highlight_info[0].get_text()
        team_size = highlight_info[1].get_text()
        location = highlight_info[2].get_text()
        print(founded)
        print(team_size)
        print(location)
        founder_cards = company_page_source.find_all('div', class_='founder-info flex-row')
        try:
            founder_name_1, founder_linkedin_1 = getFounders(founder_cards[0])
        except:
            founder_name_1 = 'NA'
            founder_linkedin_1 = 'NA'            
        try:
            founder_name_2, founder_linkedin_2 = getFounders(founder_cards[1])
        except IndexError:
            founder_name_2 = 'NA'
            founder_linkedin_2 = 'NA'
        try:
            founder_name_3, founder_linkedin_3 = getFounders(founder_cards[2])
        except IndexError:
            founder_name_3 = 'NA'
            founder_linkedin_3 = 'NA'

        print(founder_name_1, founder_linkedin_1)
        print(founder_name_2, founder_linkedin_2)
        print(founder_name_3, founder_linkedin_3)

        writer.writerow({
            headers[0]:ycomURL,
            headers[1]:company_name,
            headers[2]:company_tagline,
            headers[3]:company_description,
            headers[4]:URL,
            headers[5]:founded,
            headers[6]:team_size,
            headers[7]:location,
            headers[8]:founder_name_1,
            headers[9]:founder_linkedin_1,
            headers[10]:founder_name_2,
            headers[11]:founder_linkedin_2,
            headers[12]:founder_name_3,
            headers[13]:founder_linkedin_3,
            })

print('Mission Completed!')