from scrapy import Spider, Request
from scrapy.selector import Selector
from booking.items import BookingItem
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

class TravelokaSpider(Spider):
    name = 'traveloka1'
    allowed_domains = ['traveloka.com']
    start_urls = [
        #"https://www.traveloka.com/vi-vn/hotel/search?spec=10-07-2021.11-07-2021.1.1.HOTEL_GEO.10009843.H%C3%A0%20N%E1%BB%99i%2C%20Vi%E1%BB%87t%20Nam.2",
        #"https://www.traveloka.com/en-vn/hotel/search?spec=10-07-2021.11-07-2021.1.1.HOTEL_GEO.10010083.%C4%90%C3%A0%20N%E1%BA%B5ng%2C%20Vi%E1%BB%87t%20Nam.2",
        "https://www.traveloka.com/en-vn/hotel/search?spec=10-07-2021.11-07-2021.1.1.HOTEL_GEO.10009794.Ho%20Chi%20Minh%20City.2",
        ]
    def parse(self, response):
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--lang=id')
        options.add_argument('--disable-gpu')
        dv = webdriver.Chrome('C:/Users/MANH/Desktop/BKHN20202/Project3/Project/booking/booking/spiders/chromedriver.exe')
        dv.get(response.url)
        wait = WebDriverWait(dv, 20)
        dv.implicitly_wait(7)
        counterPage = 0
        counterHotel = 0
        wait.until(lambda dv: dv.find_element_by_css_selector('#desktopContentV3 div div:nth-child(1) div div div div div div div._2Qki3._11frB svg'))
        dv.find_element_by_css_selector('#desktopContentV3 div div:nth-child(1) div div div div div div div._2Qki3._11frB svg').click()
        nextPage = True
        wait.until(lambda dv: dv.find_element_by_css_selector('#next-button'))
        hotels = dv.find_elements_by_xpath("//div[@class='mMmI2 BN0kj tvat-searchListItem']")
        while nextPage:
            hotels = dv.find_elements_by_xpath("//div[@class='mMmI2 BN0kj tvat-searchListItem']")
            dem = 1
            print(len(hotels))
            try:
                for dem in range(len(hotels) -1 ):
                    hotel = hotels[dem]
                    counterHotel += 1
                    print(counterHotel)
                    hotel.click()
                    mainwindow = dv.window_handles[0] #tab bawaan browser
                    hotelwindow = dv.window_handles[1] #new tab
                    dv.switch_to_window(hotelwindow)
                    dv.switch_to_window(hotelwindow)
                    wait.until(lambda dv: dv.find_elements_by_xpath("//link[@rel='canonical']"))
                    wait.until(lambda dv: dv.find_elements_by_xpath("//img[@class='_1JiVE']"))
                    url = dv.current_url
                    try:
                        name = dv.find_element_by_css_selector('.tvat-hotelName').text
                    except Exception:
                        name = '-'
                    print(name)
                    try:
                        address = dv.find_element_by_css_selector('div._315kQ div.YhOlS div._1I8E_ span').text
                    except Exception:
                        address = '-'
                    try:
                        type = dv.find_element_by_css_selector('._1kzbT').text
                    except Exception:
                        type = '-'
                    try:
                        price = dv.find_element_by_xpath('//*[@id="OVERVIEW"]/div[1]/div[3]/div[2]/div[2]').text
                    except Exception:
                        price = '-'
                    try:
                        star = dv.find_element_by_css_selector('div._1RoiH._1u8y8 meta').get_attribute("content")
                    except Exception:
                        star = '-'
                    try:
                        rating = dv.find_element_by_css_selector('div._1TsnE._2M8kS div meta').get_attribute("content")
                    except Exception:
                        rating = '-'
                    try:
                        list_facilities = dv.find_elements_by_css_selector('.ImD1q')
                        facilities = [i.text for i in list_facilities]
                    except Exception:
                        facilities = '-'
                    try:
                        list_nearby_places = dv.find_elements_by_css_selector('#PLACE_NEARBY ._1dKIX')
                        nearby_places = [i.text for i in list_nearby_places]
                    except Exception:
                        nearby_places = '-'
                    try:
                        number_review = dv.find_element_by_css_selector('#REVIEW strong').text
                    except Exception:
                        number_review = '-'
                    try:
                        list_reviews = dv.find_elements_by_css_selector('.r-1yzf0co')
                        reviews = []
                        for i in range(len(list_reviews) - 1):
                            try:
                                review = {
                                'user' : dv.find_elements_by_css_selector('.r-1yzf0co')[i].find_element_by_css_selector('.r-1inkyih').text,
                                'content': dv.find_elements_by_css_selector('.r-1yzf0co')[i].find_element_by_css_selector(".r-1udh08x .r-fdjqy7").text,
                                'rating': dv.find_elements_by_css_selector('.r-1yzf0co')[i].find_element_by_css_selector(".r-1i6uqv8.r-majxgm").text,
                                }
                                reviews.append(review)
                            except NoSuchElementException:
                                continue
                    except Exception:
                        reviews = '-'
                    try:
                        time_check_in_check_out = dv.find_element_by_css_selector("b+ p").text
                    except Exception:
                        time_check_in_check_out = '-'
                    try:
                        dv.find_elements_by_css_selector('._2CntG')[0].click()
                    except Exception:
                        pass
                    try:
                        hotel_descriptions = dv.find_elements_by_css_selector('._1ZMCB p+ p')
                        hotel_descriptions = [i.text for i in hotel_descriptions]
                    except Exception:
                        hotel_descriptions = '-'
                    try:
                        dv.find_elements_by_css_selector('._2CntG')[1].click()
                    except Exception:
                        pass
                    try:
                        hotel_policy = dv.find_elements_by_css_selector('#HOTEL_POLICY')
                        hotel_policy = [i.text for i in hotel_policy]
                    except Exception:
                        hotel_policy = '-'
                    time_iso_date = datetime.now()
                    item = BookingItem()
                    item['day_crawl_check_in'] = '10/07/2021'
                    item['url'] = url
                    item['name'] = name
                    item['address'] = address
                    item['price'] = price
                    item['star'] = star
                    item['rating'] = rating
                    item['facilities'] = facilities
                    item['nearby_places'] = nearby_places
                    item['number_review'] = number_review
                    item['time_check_in_check_out'] = time_check_in_check_out
                    item['name'] = name
                    item['hotel_policy'] = hotel_policy
                    item['time_iso_date'] = time_iso_date
                    item['hotel_descriptions'] = hotel_descriptions
                    yield item
                    print(name)
                    print(address)
                    print(price)
                    print(star)
                    print(rating)
                    print(facilities)
                    print(nearby_places)
                    print(number_review)
                    print(reviews)
                    print(time_check_in_check_out)
                    print(hotel_policy)
                    dv.close()
                    dv.switch_to_window(mainwindow)
                counterPage += 1
                print(2562)
                if counterPage == 2:
                    print(485)
                    nextPage = False
                try:
                    print(151)
                    nextButton = dv.find_element_by_xpath("//div[@id='next-button']")
                except Exception:
                    print('SAii ')
                dv.execute_script('arguments[0].click();', nextButton)
                print('123')
                wait.until(lambda dv: dv.find_element_by_css_selector('#next-button'))
                print('456')
            except Exception as e:
                print("Page ", counterPage)
                print("Hotel ", counterHotel)
                print("Error next button", e)
                nextPage = False                
        print('DONE')
        dv.quit()
        del dv
    
    def parse_detail(self, response):
        item = BookingItem()
        item['day_crawl_check_in'] = "12/05/2021"
        item['url'] = response.url
        item['name'] = response.css(".tvat-hotelName::text").extract_first()
        #OVERVIEW > div._315kQ div.YhOlS div._1I8E_ span
        item['address'] = response.css("div._315kQ div.YhOlS div._1I8E_ span::text").extract_first()
        item['type'] = response.css("._1kzbT::text").extract_first()        
        #item['price'] = response.css(".r3PsG::text").extract_first()
        #item['price'] = price
        item['star'] = response.css("div._1RoiH._1u8y8 meta::attr(content)").extract_first()
        item['rating'] = response.css("div._1TsnE._2M8kS div meta::attr(content)").extract_first()
        item['facilities'] = response.css(".ImD1q::text").extract()
        #PLACE_NEARBY > div > div._2jugO > div._1NyFM > div:nth-child(1) > div:nth-child(2) div.i7zKD div span._1KrnW._1EnnQ._2HSse._1dKIX.selectorgadget_suggested
        # item['nearby_places'] = dv.find_element_by_class_name('_1dKIX').text
        item['nearby_places'] = response.css(".tvat-hotelName::text").extract_first()
        item['number_review'] =  response.css("#REVIEW strong::text").extract_first()
        reviews = Selector(response).css(".r-1yzf0co")
        item['reviews'] = []
        for i in reviews:
            review = {
                'user' : i.css('.r-1inkyih::text').extract_first(),
                'content': i.css(".r-1udh08x .r-fdjqy7::text").extract_first(),
                'rating': i.css(".r-1i6uqv8.r-majxgm::text").extract_first(),
                }
            item['reviews'].append(review)
        item['time_check_in'] = response.css("b+ p::text").extract()[0]
        item['time_check_out'] = response.css("b+ p::text").extract()[1]
        item['hotel_descriptions'] = response.css('._1ZMCB p+ p::text').extract()
        item['hotel_policy'] = response.css('#HOTEL_POLICY p::text').extract()
        item['time_iso_date'] = datetime.now()
        yield item