from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time

driver = webdriver.Chrome(
    'HotelCrawling/chromedriver')
driver.get('https://www.agoda.com/vi-vn/search?city=13170&locale=vi-vn&ckuid=a02c3325-00dd-4c8a-a74a-d4f8ce1c5da3&prid=0&currency=VND&correlationId=17e9b61b-b517-4be8-9ab2-d28e2f87566b&pageTypeId=103&realLanguageId=24&languageId=24&origin=VN&cid=-1&userId=a02c3325-00dd-4c8a-a74a-d4f8ce1c5da3&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=78&currencyCode=VND&htmlLanguage=vi-vn&cultureInfoName=vi-vn&machineName=hk-crweb-2010&trafficGroupId=4&sessionId=432llev1nb3hh0c5vxptvav1&trafficSubGroupId=4&aid=130243&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&checkIn=2021-06-01&checkOut=2021-06-02&rooms=1&adults=1&children=0&priceCur=VND&los=1&textToSearch=H%E1%BB%93%20Ch%C3%AD%20Minh&travellerType=0&familyMode=off&productType=-1')

#driver.get('https://www.agoda.com/vi-vn/search?city=13170')
n_pages = driver.find_element_by_id('paginationPageCount').text.split()[-1]
city = driver.find_element_by_css_selector('div.SearchBoxTextDescription__title').text
check_in = driver.find_element_by_css_selector('div.SearchBoxTextDescription__title[data-selenium="checkInText"]').text()
print(city)
print(n_pages)
print(check_in)

time.sleep(10)
driver.quit()
