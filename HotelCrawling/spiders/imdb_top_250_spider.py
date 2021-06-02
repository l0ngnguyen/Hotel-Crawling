import scrapy

class imdb_top_250(scrapy.Spider):
    name='imdb_top_250'

    def start_requests(self):
        urls = [
            'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating'
        ]

        for url in urls:
            yield scrapy.Request(url, callback=self.parse_query_page)

    def parse_query_page(self, response):
        detail_pages = response.css("h3.lister-item-header a")
        film_names = response.css('h3.lister-item-header a::text').getall()

        yield {'films_page': film_names}

        for page in detail_pages:
            yield response.follow(page, callback=self.parse_detail_page)

        next_query_page = response.css("div.desc a.next-page")
        if next_query_page:
            yield response.follow(next_query_page[0], callback=self.parse_query_page)


    def parse_detail_page(self, response):
        data = {}

        title_bar_wrapper = response.css("div.title_bar_wrapper")[0]
        data['title'] = title_bar_wrapper.css("div.titleBar h1::text").get()
        data['year'] = title_bar_wrapper.css("#titleYear a::text").get()

        yield data
    