import scrapy
import pandas as pd

df = pd.read_json('booking.json')
df['image_url'] = pd.Series([[] for _ in range(df.shape[0])], dtype='object')

class BookingImageCrawlingSpider(scrapy.Spider):
    name = 'booking_images'
    allowed_domains = ['booking.com']
    start_urls = df['url']

    def start_requests(self):
        for index, row in df.iterrows():
            yield scrapy.Request(row['url'], cb_kwargs={'index': index})
    
    def parse(self, response, index):
        imgs = response.css('a.bh-photo-grid-item.active-image::attr("href")').getall()
        thumbnail_imgs = response.css('a.bh-photo-grid-item.bh-photo-grid-thumb::attr("href")').getall()
        all_imgs = imgs + thumbnail_imgs

        yield {
            'index': index,
            'images': all_imgs
        }