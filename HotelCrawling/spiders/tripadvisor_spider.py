import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .cleaning import clean_text, clean_text_list, get_date_from_string
from selenium.common.exceptions import NoSuchElementException, NoSuchAttributeException
import time

def find_element_by_css_selector(driver, selector, find_more=False, attribute=None):
    """find the element by css selector and get the information that we need

    Args:
        driver (WebDriver): WebDriver selenium that we want to extract
        selector (str): the css selector 
        find_more (bool, optional): find more elements or just one. Defaults to False.
        attribute (string, optional): if attribute is None, get the text from element or get text from that attribute. Defaults to None.

    Returns:
        list, str or None: 
    """    
    try:
        if find_more:
            elements = driver.find_elements_by_css_selector(selector)
            if attribute:
                return [e.get_attribute(attribute) for e in elements]
            else:
                return [e.text for e in elements]
        else:
            element = driver.find_element_by_css_selector(selector)
            return element.get_attribute(attribute) if attribute else element.text

    except (NoSuchElementException, NoSuchAttributeException):
        return None
    except Exception:
        return None 


class TripAdvisorSpider(scrapy.Spider):
    name = 'tripadvisor'
    allowed_domains = ['tripadvisor.com.vn']
    start_urls = [
        
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

        def navigate_to_next_page(driver, wait_time=10):
            nextpage = driver.find_element_by_css_selector(
                '#search_results_table > div.bui-pagination.results-paging_simplified.js-results-paging > nav > ul > li.bui-pagination__item.bui-pagination__next-arrow > a')
            next_page_url = nextpage.get_attribute('href')
            driver.get(next_page_url)
            wait = WebDriverWait(driver, wait_time)
            wait.until(EC.url_to_be(next_page_url))

        for url in self.start_urls:
            driver = webdriver.Chrome('chromedriver')
            driver.get(url)

            city_name = 
            print(f'@crawling_in {city_name}')

            check_in = 
            check_out = 

            n_pages = 
            n_pages = int(n_pages.strip())

            for _ in range(n_pages-1):
                # get the html elements that contain infomation of hotels
                hotel_elements = 
                for hotel_element in hotel_elements:
                    hotel_link = 
                    price = 

                    yield scrapy.Request(url=hotel_link,
                                         callback=self.parse_detail,
                                         cb_kwargs={'price': price, 'check_in': check_in, 'check_out': check_out, 'city_name': city_name})

                navigate_to_next_page(driver)
            driver.quit()

    def parse_detail(self, response, price, check_in, check_out, city_name):
        hotel_name = response.css('#hp_hotel_name::text').getall()[1]
        address = response.css('span.hp_address_subtitle::text').get()
        url = response.url
        stars = len(response.css(
            '#wrap-hotelpage-top > div.hp__hotel-title > span > span.hp__hotel_ratings__stars.nowrap > span > span > span > span').getall())
        rating = response.css(
            'div.bui-review-score__badge::text').get()
        rating = rating.strip() if rating else None
        location_rating = response.css(
            '#reviewFloater > div.best-review-score.best-review-score-with_best_ugc_highlight.hp_lightbox_score_block > span > span::text').get()

        facilities = response.css(
            'div.hp_desc_important_facilities > div.important_facility::text').getall()
        facilities = clean_text_list(facilities)

        start_working_date = get_date_from_string(
            response.css('span.hp-desc-highlighted::text').get())
        description = ' '.join(response.css(
            '#property_description_content > p::text').getall())
        # nearby_places = clean_text_list(response.css(
        # 'div.bui-list__description::text').getall())
        # get the nearby places
        clusters_places_element = response.css(
            'div.hp_location_block__section_container')
        nearby_places = []
        for places_element in clusters_places_element:
            places_element = places_element.css('ul > li div.bui-list__body')
            for place_element in places_element:
                name = place_element.css(
                    'div.bui-list__description::text').get()
                if name == '\n':
                    continue
                distance = place_element.css(
                    'div.bui-list__item-action.hp_location_block__section_list_distance::text').get()
                s = name + ' ' + distance
                nearby_places.append(s)
        nearby_places = clean_text_list(nearby_places)

        n_reviews = response.css(
            'div.bui-review-score__text::text').get()
        n_reviews = n_reviews.split()[0] if n_reviews else None

        reviews = response.css(
            'ul.bui-carousel__inner > li.bui-carousel__item p > span::text').getall()
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
            'start working date': start_working_date,
            'check in': get_date_from_string(check_in),
            'check out': get_date_from_string(check_out),
            'n_reviews': n_reviews,
            'reviews': reviews,
            'facilities': facilities,
            'description': description,
            'nearby places': nearby_places
        }
