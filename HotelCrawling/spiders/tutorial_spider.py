import scrapy

class QuotesSpider(scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        urls = [
            'https://www.imdb.com/search/title/?groups=top_250&sort=user_rating'
        ]

        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        list_items = response.css("div.lister-item")

        for item in list_items:
            data = {}
            data["film_name"] = item.css("h3.lister-item-header a::text").get()
            data["year"] = item.css("h3.lister-item-header span::text").get()

            data["img_path"] = item.css("img.loadlate::attr(src)").get()
            
            data["certificate"] = item.css("span.certificate::text").get()
            data["runtime"] = item.css("span.runtime::text").get()
            data["genre"] = item.css("span.genre::text").get()

            data["rating_score"] = item.css('div.ratings-imdb-rating strong::text').get()
            data["meta_score"] = item.css('span.metascore::text').get()

            data["content_summary"] = item.css("div.ratings-bar + p.text-muted::text").get()

            data["votes_gross"] = item.css("p.sort-num_votes-visible ").css("span.text-muted + span::text").getall()

            yield data 
        
        next_page = response.css("div.desc a.next-page")[0]
        yield response.follow(next_page, callback=self.parse)












