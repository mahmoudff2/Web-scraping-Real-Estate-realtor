from scrapy import Spider,Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
import time

class My_Spider(Spider):
    name = 'realtor_family_home'

    def __init__(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless=new")
        chrome_options.add_argument("--disable-blink-features=AutomationControlled")
        chrome_options.add_argument("user-agent=GoogleOther")  
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.data = []

    def start_requests(self):
        url = 'https://www.realtor.com/realestateandhomes-search/Florida/type-single-family-home'
        yield Request(url=url, callback=self.parse,dont_filter=True,meta={'handle_httpstatus_all': True})
    
    def parse(self, response):
        self.driver.get(response.url)

        for _ in range(20):
            WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.PropertiesList_listViewGrid__8OkIX div.BasePropertyCard_propertyCardWrap__XcZ1c')))
            realstates = self.driver.find_elements(By.CSS_SELECTOR, '.PropertiesList_listViewGrid__8OkIX div.BasePropertyCard_propertyCardWrap__XcZ1c')
            # head = realstats.find_element(By.CSS_SELECTOR, '.card-description .message').text
            for element in realstates:
                price = element.find_element(By.CSS_SELECTOR, '.fMFHoW .kliDcE span').text
                rows = element.find_elements(By.CSS_SELECTOR, '.card-meta li')
                txt = []
                for row in rows:
                    try:
                        self.driver.execute_script("""
                    const parent = arguments[0];
                    const spans = parent.querySelectorAll('span[aria-hidden="true"]');
                    spans.forEach(span => span.remove());
                    """, row)
                    except:
                        continue
                    txt.append(row.text)
                try:
                    txt[0] = txt[0].replace('\n',' ')
                    txt[1] = txt[1].replace('\n',' ')
                except:
                    pass
                address = []
                address_lines = element.find_elements(By.CSS_SELECTOR, 'div.content-row div.content-col-left .truncate-line div')
                for line in address_lines:
                    address.append(line.text)
                try:
                    img = element.find_element(By.CSS_SELECTOR, '.Picture_topOnHover__MuXhx img').get_attribute('src')
                    link = element.find_element(By.CSS_SELECTOR, '.irFwYL .card-image-wrapper a').get_attribute('href')
                except:
                    img=None
                    link=None
                self.data.append({
                    'Price':price,
                    'Details':' '.join(txt),
                    'Location':' '.join(address),
                    'Image URL':img,
                    'Link':link
                })
            self.driver.execute_script("window.scrollTo(0, 0)")
            time.sleep(2)
            WebDriverWait(self.driver,10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '.next-link .button-text')))
            nxt_bt = self.driver.find_element(By.CSS_SELECTOR, '.next-link .button-text')
            nxt_bt.click()
            time.sleep(1)

        df = pd.DataFrame(self.data)
        df.columns = ['Price','Details','Location','Image URL','Link']
        with pd.ExcelWriter('output.xlsx',engine='auto') as f:
            df.to_excel(f, index=False)

    def closed(self, reason):
        self.driver.quit()