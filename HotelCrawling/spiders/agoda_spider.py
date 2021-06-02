import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException

from .cleaning import clean_text, clean_text_list, get_date_from_string
import time


class BookingSpider(scrapy.Spider):
    driver_path = '/home/long/CodeWorkspace/hotel_crawling/HotelCrawling/chromedriver'
    name = 'agoda'
    allowed_domains = ['agoda.com']
    start_urls = [
        'https://www.agoda.com/vi-vn/search?city=13170&checkIn=2021-06-01&los=1&rooms=1&adults=1&children=0&locale=vi-vn&ckuid=a02c3325-00dd-4c8a-a74a-d4f8ce1c5da3&prid=0&currency=VND&correlationId=78b6381e-aeea-4857-989e-cfc744937bdc&pageTypeId=1&realLanguageId=24&languageId=24&origin=VN&cid=-1&userId=a02c3325-00dd-4c8a-a74a-d4f8ce1c5da3&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=78&currencyCode=VND&htmlLanguage=vi-vn&cultureInfoName=vi-vn&machineName=hk-crweb-2009&trafficGroupId=4&sessionId=432llev1nb3hh0c5vxptvav1&trafficSubGroupId=4&aid=130243&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&checkOut=2021-06-02&priceCur=VND&textToSearch=H%E1%BB%93%20Ch%C3%AD%20Minh&productType=-1&travellerType=0&familyMode=off',
        'https://www.agoda.com/vi-vn/search?guid=1d9e27f2-21bd-44cb-9e48-ec79a860bdfb&asq=u2qcKLxwzRU5NDuxJ0kOF3T91go8JoYYMxAgy8FkBH1BN0lGAtYH25sdXoy34qb988fOz6NW3pFBjDYHDY7PSz4VhWJF%2FfA7zCHyWwuKnBr9E3nte9sBhqm3B9vJATxIZD8O47hhx3e0fNVEYTTe3%2BKyVS748StgJrQOYwyN3fphOBzia6AgAyy6eMTegWYgQD1m8qpi4gffzZnlfPiVVg%3D%3D&city=2758&tick=637574236249&locale=vi-vn&ckuid=a02c3325-00dd-4c8a-a74a-d4f8ce1c5da3&prid=0&currency=VND&correlationId=fa2b5819-e3d7-4249-83b4-564b05daadc2&pageTypeId=103&realLanguageId=24&languageId=24&origin=VN&cid=-1&userId=a02c3325-00dd-4c8a-a74a-d4f8ce1c5da3&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=78&currencyCode=VND&htmlLanguage=vi-vn&cultureInfoName=vi-vn&machineName=hk-crweb-2007&trafficGroupId=4&sessionId=432llev1nb3hh0c5vxptvav1&trafficSubGroupId=4&aid=130243&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&checkIn=2021-06-01&checkOut=2021-06-02&rooms=1&adults=1&children=0&priceCur=VND&los=1&textToSearch=H%C3%A0%20N%E1%BB%99i&travellerType=0&familyMode=off&productType=-1',
        'https://www.agoda.com/vi-vn/search?guid=a7e96f65-e79d-4509-92eb-1d8fcde86832&asq=u2qcKLxwzRU5NDuxJ0kOF3T91go8JoYYMxAgy8FkBH1BN0lGAtYH25sdXoy34qb9VA1aUvJl%2BlZCudawcnIWoNx%2BENZdm%2BmrzTjiiKONhAtN%2FyMUyP07NJv%2BgqhHtt6hG5stZZscvjQurvqGHKlLj9lB5GLJpJoRnckeclAbBbZxcP47HWDCW8h37XlkBeaatQDL6afeOLVFlrg86NELVQ%3D%3D&city=16440&tick=637574236549&locale=vi-vn&ckuid=a02c3325-00dd-4c8a-a74a-d4f8ce1c5da3&prid=0&currency=VND&correlationId=15a7a028-41d8-4f21-a0f1-d1aa9f2728b4&pageTypeId=103&realLanguageId=24&languageId=24&origin=VN&cid=-1&userId=a02c3325-00dd-4c8a-a74a-d4f8ce1c5da3&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=78&currencyCode=VND&htmlLanguage=vi-vn&cultureInfoName=vi-vn&machineName=hk-crweb-2013&trafficGroupId=4&sessionId=432llev1nb3hh0c5vxptvav1&trafficSubGroupId=4&aid=130243&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&checkIn=2021-06-01&checkOut=2021-06-02&rooms=1&adults=1&children=0&priceCur=VND&los=1&textToSearch=%C4%90%C3%A0%20N%E1%BA%B5ng&productType=-1&travellerType=0&familyMode=off',
        'https://www.agoda.com/vi-vn/search?guid=f97514d5-4454-4308-8eeb-1097c7523616&asq=u2qcKLxwzRU5NDuxJ0kOF3T91go8JoYYMxAgy8FkBH1BN0lGAtYH25sdXoy34qb9%2BXy%2FahGHsKErffSXhwgq67LW28e8O01%2Bh4gj%2B4mCbAhAb6abzBAVbDYBn9QMx1VDikrSP3cx4715NAYXt0MMqXoqtprCQ3gsAWh8zCwMNFSPrNCzaUcUd6dYKjG47LjOqJjqosfxFy3LMNu2M9lHcw%3D%3D&city=15932&tick=637574236829&locale=vi-vn&ckuid=a02c3325-00dd-4c8a-a74a-d4f8ce1c5da3&prid=0&currency=VND&correlationId=df48ab64-2aea-4abd-9fb8-b905197cecb8&pageTypeId=103&realLanguageId=24&languageId=24&origin=VN&cid=-1&userId=a02c3325-00dd-4c8a-a74a-d4f8ce1c5da3&whitelabelid=1&loginLvl=0&storefrontId=3&currencyId=78&currencyCode=VND&htmlLanguage=vi-vn&cultureInfoName=vi-vn&machineName=hk-crweb-2028&trafficGroupId=4&sessionId=432llev1nb3hh0c5vxptvav1&trafficSubGroupId=4&aid=130243&useFullPageLogin=true&cttp=4&isRealUser=true&mode=production&checkIn=2021-06-01&checkOut=2021-06-02&rooms=1&adults=1&children=0&priceCur=VND&los=1&textToSearch=%C4%90%C3%A0%20L%E1%BA%A1t&travellerType=0&familyMode=off&productType=-1'
    ]
    citys = ['Hồ Chí Minh', 'Hà Nội', 'Đà Nẵng', 'Đà Lạt']

    def start_requests(self):
        yield scrapy.Request(self.start_urls[0], callback=self.parse_links)

    def parse_links(self, response):
        """[summary]
            firstly: extract all hotel links from a hotel list page
            secondly: make a request for every hotel links and the handle the every return hotel detail page by parse_detail method
            thirdly: navigate to the next hotel list page to continue the job
        Args:
            response ([type]): [description]
        """

        def navigate_to_next_page(driver):
            nextpage = driver.find_element_by_id('paginationNext')
            nextpage.click()
            scroll_down_page(driver, 1000)

        def scroll_down_page(driver, speed=100):
            time.sleep(2)
            current_scroll_position, new_height = 0, 1
            while current_scroll_position <= new_height:
                current_scroll_position += speed
                driver.execute_script(
                    "window.scrollTo(0, {});".format(current_scroll_position))
                time.sleep(1)
                new_height = driver.execute_script(
                    "return document.body.scrollHeight")

        for url in self.start_urls:
            driver = webdriver.Chrome(self.driver_path)
            driver.get(url)

            scroll_down_page(driver, 1000)

            city_name = driver.find_element_by_css_selector(
                'div.SearchBoxTextDescription__title').text
            print(f'@crawling_in {city_name}')

            '''
            check_in = driver.find_element_by_css_selector(
                'div.SearchBoxTextDescription__title[data-selenium="checkInText"]').text
            check_out = driver.find_element_by_css_selector(
                'div.SearchBoxTextDescription__title[data-selenium="checkOutText"]').text
            '''
            check_in = '1/6/2021'
            check_out = '2/6/2021'

            n_pages = driver.find_element_by_id(
                'paginationPageCount').text.split()[-1]
            n_pages = int(n_pages)

            for _ in range(n_pages-1):
                print(f'@page {n_pages}')
                # get the html elements that contain infomation of hotels
                hotel_elements = driver.find_elements_by_css_selector(
                    'li.PropertyCard.PropertyCardItem[data-selenium="hotel-item"]')
                for hotel_element in hotel_elements:
                    try:
                        hotel_link = hotel_element.find_element_by_css_selector(
                            'a.PropertyCard__Link').get_attribute('href')
                        price = hotel_element.find_element_by_css_selector(
                            'span.PropertyCardPrice__Value').text
                    except Exception:
                        hotel_link = ''
                        price = -1

                    try:
                        hotel_name = hotel_element.find_element_by_css_selector(
                            'h3.PropertyCard__HotelName').text
                    except NoSuchElementException:
                        hotel_name = ''

                    try:
                        n_reviews = hotel_element.find_element_by_css_selector(
                            'span.sc-jSgupP.iWPxuo.sc-bdfBwQ.hgXzCN').text
                        rating = hotel_element.find_element_by_css_selector(
                            'h4.sc-gInsOo.hCHQcj.kite-js-Typography').text
                    except NoSuchElementException:
                        n_reviews = 0
                        rating = None

                    try:
                        image = hotel_element.find_element_by_css_selector(
                            'img.HeroImage.HeroImage--s').get_attribute('src')
                    except NoSuchElementException:
                        image = None

                    try:
                        location_rating = hotel_element.find_element_by_css_selector(
                            'div.sc-bdfBwQ.jRrPAL > p').text.split()[-1]
                    except NoSuchElementException:
                        location_rating = None

                    if hotel_link:

                        '''
                        driver.execute_script(
                            f'window.open("{hotel_link}","_blank");')
                        driver.switch_to.window(driver.window_handles[-1])
                        time.sleep(5)

                        yield self.parse_detail_by_selenium(driver, hotel_link, price, check_in, check_out, city_name)

                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        '''
                        yield scrapy.Request(url=hotel_link,
                                             callback=self.parse_detail,
                                             cb_kwargs={'price': price,
                                                        'check_in': check_in,
                                                        'check_out': check_out,
                                                        'city_name': city_name,
                                                        'hotel_name': hotel_name,
                                                        'rating': rating,
                                                        'location_rating': location_rating,
                                                        'n_reviews': n_reviews,
                                                        'image': image})

                navigate_to_next_page(driver)
            driver.quit()

    def parse_detail_by_selenium(self, driver, hotel_link, price, check_in, check_out, city_name):
        hotel_name = driver.find_element_by_css_selector(
            'h1.HeaderCerebrum__Name').text
        address = driver.find_element_by_css_selector(
            'span[data-selenium="hotel-address-map"]').text
        url = hotel_link

        try:
            stars = driver.find_element_by_css_selector(
                'i[data-selenium="mosaic-hotel-rating"]').get_attribute('class')
            stars = stars.split()[3].split('-')[-1]
        except NoSuchElementException:
            stars = 0

        rating = driver.find_element_by_css_selector(
            'span.ReviewScore-Number[data-selenium="hotel-header-review-score"]').text
        #rating = rating.strip() if rating else None

        location_rating = driver.find_element_by_css_selector(
            'span.sc-jSgupP.gfEOpa').text

        try:
            facilities = [e.text for e in driver.find_elements_by_css_selector(
                'p.FavFeatures__Text.FavFeatures__Text--small')]
        except NoSuchElementException:
            facilities = []

        try:
            description = driver.find_element_by_css_selector(
                'p.sc-bZSQDF.galQQu').text
        except NoSuchElementException:
            description = ''

        nearby_places = [
            e.text for e in driver.find_elements_by_css_selector('li.poi-item')]

        try:
            n_reviews = driver.find_element_by_css_selector(
                'div.review-basedon span.text').text
        except NoSuchElementException:
            n_reviews = ''

        try:
            reviews = [e.text for e in driver.find_elements_by_css_selector(
                'p.Review-comment-bodyText')]
        except NoSuchElementException:
            reviews = 0

        return {
            'city': city_name,
            'hotel name': clean_text(hotel_name),
            'url': url,
            'address': clean_text(address),
            'stars': stars,
            'price': price,
            'rating': rating,
            'location rating': clean_text(location_rating),
            # 'start working date': start_working_date,
            'check in': check_in,
            'check out': check_out,
            'n_reviews': n_reviews,
            'reviews': reviews,
            'facilities': facilities,
            'description': description,
            'nearby places': nearby_places
        }

    def parse_detail(self, response, price, check_in, check_out, city_name, hotel_name, rating, location_rating, n_reviews, image):
        address = response.css(
            'span[data-selenium="hotel-address-map"]::text').get()
        url = response.url

        stars = response.css(
            'i[data-selenium="mosaic-hotel-rating"]::attr("class")').get()
        stars = stars.split()[3].split('-')[-1] if stars else 0

        facilities = response.css(
            'p.FavFeatures__Text.FavFeatures__Text--small::text').getall()
        facilities = clean_text_list(facilities)

        nearby_places = response.css('li.poi-item::text').getall()

        reviews = response.css('p.Review-comment-bodyText::text').getall()
        reviews = [clean_text(review)
                   for review in reviews] if len(reviews) > 0 else []

        yield {
            'city': city_name,
            'hotel name': clean_text(hotel_name),
            'url': url,
            'address': clean_text(address),
            'stars': stars,
            'price': price,
            'rating': rating,
            'location rating': clean_text(location_rating),
            'check in': check_in,
            'check out': check_out,
            'n_reviews': n_reviews,
            'image': image,
            'reviews': reviews,
            'facilities': facilities,
            'nearby places': nearby_places
        }
