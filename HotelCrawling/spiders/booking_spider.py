import scrapy
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .utils import clean_text, clean_text_list, get_date_from_string


class BookingSpider(scrapy.Spider):
    name = 'booking.com'
    allowed_domains = ['booking.com']
    start_urls = [
        'https://www.booking.com/searchresults.vi.html?aid=309654&label=hotels-vietnamese-vi-84rnFuf*4DmuoNwHXr9HuwS506720659338%3Apl%3Ata%3Ap1%3Ap2%3Aac%3Aap%3Aneg%3Afi%3Atiaud-922652055822%3Akwd-17241331%3Alp9040331%3Ali%3Adec%3Adm&sid=da261bbfb6a1c1b9c342b8ad94b35079&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.vi.html%3Faid%3D309654%3Blabel%3Dhotels-vietnamese-vi-84rnFuf*4DmuoNwHXr9HuwS506720659338%253Apl%253Ata%253Ap1%253Ap2%253Aac%253Aap%253Aneg%253Afi%253Atiaud-922652055822%253Akwd-17241331%253Alp9040331%253Ali%253Adec%253Adm%3Bsid%3Dda261bbfb6a1c1b9c342b8ad94b35079%3Btmpl%3Dsearchresults%3Bcheckin_monthday%3D19%3Bcheckin_year_month%3D2021-05%3Bcheckout_monthday%3D20%3Bcheckout_year_month%3D2021-05%3Bclass_interval%3D1%3Bdest_id%3D-3730078%3Bdest_type%3Dcity%3Bdr_ps%3DISR%3Bdtdisc%3D0%3Bfrom_history%3D1%3Bgroup_adults%3D1%3Bgroup_children%3D0%3Bhighlighted_hotels%3D5739875%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Border%3Dpopularity%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%3Bsb_price_type%3Dtotal%3Bsh_position%3D1%3Bshw_aparth%3D1%3Bsi%3Dai%3Bsi%3Dci%3Bsi%3Dco%3Bsi%3Ddi%3Bsi%3Dla%3Bsi%3Dre%3Bslp_r_match%3D0%3Bsrpvid%3D2a7772357489013c%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%3Btop_ufis%3D1%3Bsig%3Dv1k-XrHeOj%3B&highlighted_hotels=5739875&order=popularity&ss=TP.+H%C3%B4%CC%80+Chi%CC%81+Minh&is_ski_area=0&ssne=TP.+H%C3%B4%CC%80+Chi%CC%81+Minh&ssne_untouched=TP.+H%C3%B4%CC%80+Chi%CC%81+Minh&dest_id=-3730078&dest_type=city&checkin_year=2021&checkin_month=5&checkin_monthday=20&checkout_year=2021&checkout_month=5&checkout_monthday=21&group_adults=1&group_children=0&no_rooms=1&sb_changed_dates=1&from_sf=1',
        'https://www.booking.com/searchresults.vi.html?aid=304142&label=gen173nr-1DCAEoggI46AdIM1gEaPQBiAEBmAEquAEZyAEM2AED6AEBiAIBqAIDuAKI0pOFBsACAdICJDA0ZDY0YjU1LTc1Y2UtNDRhNy05MTIyLWM5OGY3ZWEzOTY2NNgCBOACAQ&sid=da261bbfb6a1c1b9c342b8ad94b35079&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.vi.html%3Faid%3D304142%3Blabel%3Dgen173nr-1DCAEoggI46AdIM1gEaPQBiAEBmAEquAEZyAEM2AED6AEBiAIBqAIDuAKI0pOFBsACAdICJDA0ZDY0YjU1LTc1Y2UtNDRhNy05MTIyLWM5OGY3ZWEzOTY2NNgCBOACAQ%3Bsid%3Dda261bbfb6a1c1b9c342b8ad94b35079%3Btmpl%3Dsearchresults%3Bcheckin_monthday%3D19%3Bcheckin_year_month%3D2021-05%3Bcheckout_monthday%3D20%3Bcheckout_year_month%3D2021-05%3Bclass_interval%3D1%3Bdest_id%3D-3714993%3Bdest_type%3Dcity%3Bdr_ps%3DISR%3Bdtdisc%3D0%3Bfrom_history%3D1%3Bgroup_adults%3D1%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Border%3Dpopularity%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%3Bsb_price_type%3Dtotal%3Bsh_position%3D3%3Bshw_aparth%3D1%3Bsi%3Dai%3Bsi%3Dci%3Bsi%3Dco%3Bsi%3Ddi%3Bsi%3Dla%3Bsi%3Dre%3Bslp_r_match%3D0%3Bsrpvid%3De682760dc1900178%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%3Btop_ufis%3D1%3Bsig%3Dv1f1pFvCIf%3B&order=popularity&ss=Ha%CC%80+N%C3%B4%CC%A3i&is_ski_area=0&ssne=Ha%CC%80+N%C3%B4%CC%A3i&ssne_untouched=Ha%CC%80+N%C3%B4%CC%A3i&dest_id=-3714993&dest_type=city&checkin_year=2021&checkin_month=5&checkin_monthday=20&checkout_year=2021&checkout_month=5&checkout_monthday=21&group_adults=1&group_children=0&no_rooms=1&sb_changed_dates=1&from_sf=1',
        'https://www.booking.com/searchresults.vi.html?aid=304142&label=gen173nr-1DCAEoggI46AdIM1gEaPQBiAEBmAEquAEZyAEM2AED6AEBiAIBqAIDuALywJSFBsACAdICJGU0MmE1OGU2LTliYTMtNGVlOC05NTAwLTY5ZmE3YTQ5YTc3YtgCBOACAQ&sid=da261bbfb6a1c1b9c342b8ad94b35079&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.vi.html%3Faid%3D304142%3Blabel%3Dgen173nr-1DCAEoggI46AdIM1gEaPQBiAEBmAEquAEZyAEM2AED6AEBiAIBqAIDuALywJSFBsACAdICJGU0MmE1OGU2LTliYTMtNGVlOC05NTAwLTY5ZmE3YTQ5YTc3YtgCBOACAQ%3Bsid%3Dda261bbfb6a1c1b9c342b8ad94b35079%3Btmpl%3Dsearchresults%3Bcheckin_month%3D5%3Bcheckin_monthday%3D19%3Bcheckin_year%3D2021%3Bcheckout_month%3D5%3Bcheckout_monthday%3D20%3Bcheckout_year%3D2021%3Bcity%3D-3712125%3Bclass_interval%3D1%3Bdest_id%3D-3712125%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bfrom_sf%3D1%3Bgroup_adults%3D1%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%3Brows%3D25%3Bsb_price_type%3Dtotal%3Bshw_aparth%3D1%3Bslp_r_match%3D0%3Bsrc%3Dsearchresults%3Bsrc_elem%3Dsb%3Bsrpvid%3Df575723e9d88010a%3Bss%3D%25C4%2590%25C3%25A0%2BN%25E1%25BA%25B5ng%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%3Bssne%3D%25C4%2590%25C3%25A0%2BN%25E1%25BA%25B5ng%3Bssne_untouched%3D%25C4%2590%25C3%25A0%2BN%25E1%25BA%25B5ng%3Btop_ufis%3D1%3Bsig%3Dv1xHRiTJMt%3B&ss=%C4%90%C3%A0+N%E1%BA%B5ng&is_ski_area=0&ssne=%C4%90%C3%A0+N%E1%BA%B5ng&ssne_untouched=%C4%90%C3%A0+N%E1%BA%B5ng&dest_id=-3712125&dest_type=city&checkin_year=2021&checkin_month=5&checkin_monthday=20&checkout_year=2021&checkout_month=5&checkout_monthday=21&group_adults=1&group_children=0&no_rooms=1&sb_changed_dates=1&from_sf=1',
        'https://www.booking.com/searchresults.vi.html?aid=304142&label=gen173nr-1DCAEoggI46AdIM1gEaPQBiAEBmAEquAEZyAEM2AED6AEBiAIBqAIDuALywJSFBsACAdICJGU0MmE1OGU2LTliYTMtNGVlOC05NTAwLTY5ZmE3YTQ5YTc3YtgCBOACAQ&sid=da261bbfb6a1c1b9c342b8ad94b35079&sb=1&src=searchresults&src_elem=sb&error_url=https%3A%2F%2Fwww.booking.com%2Fsearchresults.vi.html%3Faid%3D304142%3Blabel%3Dgen173nr-1DCAEoggI46AdIM1gEaPQBiAEBmAEquAEZyAEM2AED6AEBiAIBqAIDuALywJSFBsACAdICJGU0MmE1OGU2LTliYTMtNGVlOC05NTAwLTY5ZmE3YTQ5YTc3YtgCBOACAQ%3Bsid%3Dda261bbfb6a1c1b9c342b8ad94b35079%3Btmpl%3Dsearchresults%3Bcheckin_year_month_monthday%3D2021-05-19%3Bcheckout_year_month_monthday%3D2021-05-20%3Bclass_interval%3D1%3Bdest_id%3D-3712045%3Bdest_type%3Dcity%3Bdtdisc%3D0%3Bgroup_adults%3D1%3Bgroup_children%3D0%3Binac%3D0%3Bindex_postcard%3D0%3Blabel_click%3Dundef%3Bno_rooms%3D1%3Boffset%3D0%3Bpostcard%3D0%3Braw_dest_type%3Dcity%3Broom1%3DA%3Bsb_price_type%3Dtotal%3Bshw_aparth%3D1%3Bslp_r_match%3D0%3Bsrpvid%3D28ee7244d7bf0115%3Bss_all%3D0%3Bssb%3Dempty%3Bsshis%3D0%3Btop_ufis%3D1%3Bsig%3Dv1dFK5xArA%3B&ss=%C4%90%C3%A0+L%E1%BA%A1t&is_ski_area=0&ssne=%C4%90%C3%A0+L%E1%BA%A1t&ssne_untouched=%C4%90%C3%A0+L%E1%BA%A1t&dest_id=-3712045&dest_type=city&checkin_year=2021&checkin_month=5&checkin_monthday=20&checkout_year=2021&checkout_month=5&checkout_monthday=21&group_adults=1&group_children=0&no_rooms=1&sb_changed_dates=1&from_sf=1'
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
            driver = webdriver.Chrome(
                'HotelCrawling/chromedriver')
            driver.get(url)

            city_name = driver.find_element_by_css_selector(
                '#right > div:nth-child(2) > div > div.sr_header--title > div > h1').text
            city_name = city_name.split(':')[0]
            print(f'@crawling_in {city_name}')

            check_in_out_element = driver.find_elements_by_css_selector(
                'div.sb-date-field__display')
            check_in, check_out = [
                datetime.text for datetime in check_in_out_element]

            n_pages = driver.find_element_by_css_selector(
                'ul.bui-pagination__list li:last-child div.bui-u-inline').text
            n_pages = int(n_pages.strip())

            for _ in range(n_pages-1):
                # get the html elements that contain infomation of hotels
                hotel_elements = driver.find_elements_by_css_selector(
                    'div.sr_item_content.sr_item_content_slider_wrapper')
                for hotel_element in hotel_elements:
                    hotel_link = hotel_element.find_element_by_css_selector(
                        'a.hotel_name_link').get_attribute('href')
                    price = hotel_element.find_element_by_css_selector(
                        'div.bui-price-display__value.prco-inline-block-maker-helper').text

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
